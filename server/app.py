from flask import Flask, render_template, session, jsonify, request, send_file, g
from participant import Participant
from flask_socketio import SocketIO, emit
import threading
import time
import uuid
from api_handler import modify_weights, get_api_key
import matplotlib.pyplot as plt
import os


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling

# Store active users and their statuses
connected_users = set()  # Track connected users
user_status = {}  # Map user_id to their matchmaking status ('waiting', 'matched', etc.)
lock = threading.Lock()  # Lock for thread-safe access

# Initialize SocketIO
socketio = SocketIO(app)
acceptances = 0
people_first_round = []
selected_first_round = []
people_second_round = []

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
        if not selected_first_round and people_first_round:
            selected_first_round.append(people_first_round[0])
            
            for user_id in people_first_round:
                if user_id != selected_first_round[0]:
                    # Invert the user status
                    user_status[user_id] = 'waiting' if user_status[user_id] == 'interaction' else 'interaction'
                    print(f"User {user_id} status: {user_status[user_id]}")

    with lock:
        # Add the user to connected_users
        connected_users.add(g.user_id)

        # Ensure the user hasn't been added already
        if g.user_id not in user_status:
            if len(people_first_round) < 2:
                # If the first round is not full, add the user
                people_first_round.append(g.user_id)
                user_status[g.user_id] = 'interaction'  # Set to 'interaction' for first round
            
    print(f"First round users: {people_first_round}")
    print(f"Second round users: {selected_first_round}")
    print(f"User statuses: {user_status}")

    return render_template('matchmaking.html')



@app.route('/matchmaking_done')
def matchmaking_done():
    global people_first_round, selected_first_round, people_second_round
    """Serve the page corresponding to the user's status."""
    with lock:
        if sum([1 for status in user_status.values() if status == 'interaction']) == 3 and ((not selected_first_round) or selected_first_round[0] != g.user_id):
            # If two users are in the 'interaction' status, set their status to 'matched'
            user_status[g.user_id] = 'waiting'
            selected_first_round.clear()
            selected_first_round = [user_id for user_id in people_first_round if user_id != g.user_id]

    status = user_status.get(g.user_id, 'waiting')
        
    print(f"First round users: {people_first_round}")
    print(f"Second round users: {selected_first_round}")
    print(f"User statuses: {user_status}")

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
    if acceptances == 2:
        emit('redirect_to_congratulations', {'message': 'Both users accepted the match'}, broadcast=True)


@app.route('/clear_acceptances', methods=['POST'])
def clear_acceptances():
    global acceptances, connected_users
    acceptances = 0
    connected_users = set()
    return '', 200  # Simply return 200 with an empty response

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

"""def trigger_matchmaking():
    Perform matchmaking when conditions are met.
    print("Matchmaking triggered!")
    with lock:
        for user_id in connected_users:
            user_status[user_id] = 'waiting'"""


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback = data.get('feedback')
    print(f"Received feedback: {feedback}")

    # Example feature importance dictionary
    feature_importance = {"skill_similitude": 0.6, "objective_similitude": 0.5}

    api_key = get_api_key()

    # Modify the feature importance based on the feedback
    new_feature_importance = modify_weights(api_key, feature_importance, feedback)

    # Generate barplot
    generate_barplot(feature_importance, new_feature_importance)

    # Send back the response with the path to the image
    return jsonify({'message': 'Feedback received!', 'barplot_url': '/get_barplot'}), 200


@app.route('/get_barplot')
def get_barplot():
    return send_file('static/feature_importance.png', mimetype='image/png')


def generate_barplot(feature_importance, new_feature_importance):
    # Ensure the 'static' directory exists
    static_dir = 'server/static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35

    indices = range(len(feature_importance))

    ax.bar(
        indices,
        feature_importance.values(),
        width=width,
        label='Original',
        color='skyblue'
    )
    ax.bar(
        [i + width for i in indices],
        new_feature_importance.values(),
        width=width,
        label='Updated',
        color='orange'
    )

    ax.set_xlabel('Features')
    ax.set_ylabel('Importance')
    ax.set_title('Feature Importance Comparison')
    ax.set_xticks([i + width / 2 for i in indices])
    ax.set_xticklabels(feature_importance.keys(), rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()

    barplot_path = os.path.join(static_dir, 'feature_importance.png')
    plt.savefig(barplot_path)
    plt.close()

    # Ensure the file is ready
    for _ in range(10):  # Retry for up to 1 second
        if os.path.exists(barplot_path):
            break
        time.sleep(0.1)

    return f'/{barplot_path}'
    

# Background thread to monitor matchmaking
"""def matchmaking_monitor():
    This function will run continuously in the background, checking for matchmaking conditions.
    while True:
        try:
            trigger_matchmaking()  # Trigger matchmaking every 5 seconds
            # Stop the thread 
            break
        except Exception as e:
            print(f"Error during matchmaking: {e}")
        time.sleep(5)  # Check every 5 seconds"""

# Start matchmaking monitor thread in the background
#matchmaking_thread = threading.Thread(target=matchmaking_monitor, daemon=True)
#matchmaking_thread.start()

# Start the Flask app
socketio.run(app, host='0.0.0.0', port=5000, debug=True)