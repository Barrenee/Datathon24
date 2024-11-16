from flask import Flask, render_template, session, jsonify, request, send_file, g
from participant import Participant
import threading
import time
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling

# Store active users
connected_users = set()  # Use a set to avoid duplicates
lock = threading.Lock()  # To avoid race conditions when updating `connected_users`


# Middleware to check user activity
@app.before_request
def track_user_activity():
    if 'user_id' not in session:
        session['user_id'] = str(generate_user_id())  # Assign a unique ID
    g.user_id = session['user_id']

def generate_user_id():
    return uuid.uuid4()


@app.route('/leave_matchmaking', methods=['POST'])
def leave_matchmaking():
    with lock:
        connected_users.discard(g.user_id)  # Remove user from the connected list
    return jsonify({'message': 'User removed from matchmaking'}), 200


@app.route('/connected_users', methods=['GET'])
def get_connected_users():
    with lock:
        print(connected_users)
        return jsonify({'connected_users': len(connected_users)}), 200

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/script_get_inscription')
def script_get_inscription():
    return send_file('./scripts/get_inscription.js')

@app.route('/matchmaking_html')
def matchmaking_html():
    with lock:
        connected_users.add(g.user_id) 
    return render_template('matchmaking.html')

@app.route('/script_matchmaking')
def script_matchmaking():
    return send_file('./scripts/matchmaking.js')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.is_json:  # Check if the request is indeed JSON
        # Get the JSON data from the request
        data = request.get_json()

        print("Receiving data from the form:")
        print(data)  # For debugging, print the received data
        
        # From programming skills, remove all the skills that have a 0 value
        data['programming_skills'] = {skill: value for skill, value in data['programming_skills'].items() if value != 0}
        
        print("Processed data:")
        person = Participant(**data)

        print(person)  # For debugging, print the processed data


        return jsonify({'message': 'Form submitted successfully!', 'data': data}), 200
    else:
        return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 415


app.run(host='0.0.0.0', port=5000, debug=True)
