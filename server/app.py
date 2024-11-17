from flask import Flask, render_template, session, jsonify, request, send_file, g
from participant import Participant
import threading
import time
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling

# Store active users and their statuses
connected_users = set()  # Track connected users
user_status = {}  # Map user_id to their matchmaking status ('waiting', 'matched', etc.)
lock = threading.Lock()  # Lock for thread-safe access

# Middleware to track user activity
@app.before_request
def track_user_activity():
    if 'user_id' not in session:
        session['user_id'] = str(generate_user_id())  # Assign a unique ID
    g.user_id = session['user_id']

def generate_user_id():
    return uuid.uuid4()

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
            user_status[g.user_id] = 'waiting'  # Default status when joining
    return render_template('matchmaking.html')

@app.route('/matchmaking_done')
def matchmaking_done():
    """Serve the page corresponding to the user's status."""
    with lock:
        # Default to 'waiting' if user is not yet processed
        status = user_status.get(g.user_id, 'waiting')
    return render_template(f"{status}.html")

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/script_get_inscription')
def script_get_inscription():
    return send_file('./scripts/get_inscription.js')

@app.route('/script_matchmaking')
def script_matchmaking():
    return send_file('./scripts/matchmaking.js')

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
        if len(connected_users) >= 3:  # Example condition: 3 or more users
            matched_users = list(connected_users)[:3]  # Take 3 users to match
            for user in matched_users:
                user_status[user] = 'matched'
                connected_users.remove(user)
            print(f"Matched users: {matched_users}")
        else:
            # Reset all waiting users to continue waiting
            for user in connected_users:
                user_status[user] = 'waiting'

# Background thread to monitor matchmaking
def matchmaking_monitor():
    """This function will run continuously in the background, checking for matchmaking conditions."""
    while True:
        try:
            trigger_matchmaking()  # Trigger matchmaking every 5 seconds
        except Exception as e:
            print(f"Error during matchmaking: {e}")
        time.sleep(5)  # Check every 5 seconds

# Start matchmaking monitor thread in the background
matchmaking_thread = threading.Thread(target=matchmaking_monitor, daemon=True)
matchmaking_thread.start()

# Start the Flask app
app.run(host='0.0.0.0', port=5000, debug=True)
