from flask import Flask, render_template, session, jsonify, request, send_file, g
from participant import Participant
from flask_socketio import SocketIO, emit
import threading
import time
import uuid
from api_handler import modify_weights
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling

# Store active users and their statuses
connected_users = set()  # Track connected users
user_status = {}  # Map user_id to their matchmaking status ('waiting', 'matched', etc.)
lock = threading.Lock()  # Lock for thread-safe access

# Initialize SocketIO
socketio = SocketIO(app)
acceptances = 0

# Middleware to track user activity
@app.before_request
def track_user_activity():
    if 'user_id' not in session:
        session['user_id'] = str(generate_user_id())  # Assign a unique ID
    g.user_id = session['user_id']

def generate_user_id():
    return uuid.uuid4()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/leave_matchmaking', methods=['POST'])
def leave_matchmaking():
    """Remove user from matchmaking and reset their status."""
    with lock:
        connected_users.discard(g.user_id)
        user_status.pop(g.user_id, None)  # Remove user's status if it exists
    return jsonify({'message': 'User removed from matchmaking'}), 200

@app.route('/connected_users', methods=['GET'])
def get_connected_users():
    """Return the count of connected users."""
    with lock:
        return jsonify({'connected_users': len(connected_users)}), 200

@app.route('/matchmaking_html')
def matchmaking_html():
    """Add the user to matchmaking and set their status."""
    with lock:
        connected_users.add(g.user_id)
        if g.user_id not in user_status:
            user_status[g.user_id] = 'interaction'  # Default status when joining
    return render_template('matchmaking.html')

@app.route('/matchmaking_done')
def matchmaking_done():
    """Serve the page corresponding to the user's status."""
    with lock:
        # Default to 'waiting' if user is not yet processed
        status = user_status.get(g.user_id, 'interaction')
    return render_template(f"{status}.html")


# SOCKET.IO EVENTS
@socketio.on('connect')
def handle_connect():
    user_id = session.get('user_id')
    print(f"User {user_id} connected.")
    connected_users.add(user_id)

@socketio.on('send_message')
def handle_message(data):
    user_id = session.get('user_id')
    if not user_id:
        print("User is not authenticated.")
        return

    print(f"Received message from user {user_id}: {data['message']}")
    emit('receive_message', {
        'user_id': user_id,
        'message': data['message'],
    }, broadcast=True, include_self=False)

# Handle the reject match event from any user
@socketio.on('reject_match')
def handle_reject_match():
    # You can use g.user_id or socket.id to track the rejecting user
    print(f"User rejected the match.")  # Logs the rejection, using g.user_id

    # Perform any necessary actions after rejection
    # For example, you could broadcast this rejection to others:
    emit('redirect_to_why', {'message': 'One of the users rejected the match'}, broadcast=True)

@socketio.on('accept_match')
def handle_accept_match():
    global acceptances
    acceptances += 1
    print(f"User accepted the match. Acceptances: {acceptances}")
    if acceptances == 1:
        emit('redirect_to_congratulations', {'message': 'Both users accepted the match'}, broadcast=True)




# ROUTES
@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/interaction')
def interaction():
    return render_template('interaction.html')

@app.route('/script_get_inscription')
def script_get_inscription():
    return send_file('./scripts/get_inscription.js')

@app.route('/script_matchmaking')
def script_matchmaking():
    return send_file('./scripts/matchmaking.js')

@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')

@app.route('/script_interaction')
def script_interaction():
    return send_file('./scripts/interaction.js')

@app.route('/why')
def why():
    return render_template('why.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    """Handle form submission and print received data."""
    if request.is_json:
        data = request.get_json()

        print("Receiving data from the form:")
        print(data)  # For debugging

        # Remove skills with zero value
        data['programming_skills'] = {
            skill: value for skill, value in data['programming_skills'].items() if value != 0
        }

        person = Participant(**data)
        print("Processed data:")
        print(person)

        return jsonify({'message': 'Form submitted successfully!', 'data': data}), 200
    else:
        return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 415

def trigger_matchmaking():
    """Perform matchmaking when conditions are met."""
    print("Matchmaking triggered!")
    with lock:
        for user_id in connected_users:
            user_status[user_id] = 'interaction'


# Insight processing:
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = data.get('feedback')
    print(f"Received feedback: {feedback}")

    # Example feature importance dictionary
    feature_importance = {"skill_similitude": 0.6, "objective_similitude": 0.5}

    # Modify the feature importance based on the feedback
    with open("server/api_key.txt", "a") as f:
        api_key = f.readline()
    new_feature_importance = modify_weights(api_key, feature_importance, feedback)

    # Generate barplot
    barplot_path = generate_barplot(feature_importance, new_feature_importance)

    # Return the URL of the barplot
    return jsonify({"barplot_url": barplot_path})

def generate_barplot(feature_importance, new_feature_importance):
    # Plot both feature importances in the same barplot

    fig, ax = plt.subplots()
    ax.bar(feature_importance.keys(), feature_importance.values(), label='Original')
    ax.bar(new_feature_importance.keys(), new_feature_importance.values(), label='Updated')
    ax.set_ylabel('Importance')
    ax.set_title('Feature Importance')
    ax.legend()

    # Save the plot to a file
    barplot_path = 'static/feature_importance.png'
    plt.savefig(barplot_path)
    plt.close()
    

# Background thread to monitor matchmaking
def matchmaking_monitor():
    """This function will run continuously in the background, checking for matchmaking conditions."""
    while True:
        try:
            trigger_matchmaking()  # Trigger matchmaking every 5 seconds
            # Stop the thread 
            break
        except Exception as e:
            print(f"Error during matchmaking: {e}")
        time.sleep(5)  # Check every 5 seconds

# Start matchmaking monitor thread in the background
matchmaking_thread = threading.Thread(target=matchmaking_monitor, daemon=True)
matchmaking_thread.start()

# Start the Flask app
socketio.run(app, host='0.0.0.0', port=5000, debug=True)