from flask import Flask, render_template, session, jsonify, request, send_file

app = Flask(__name__)

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

@app.route('/matchmaking')
def matchmaking():
    return render_template('matchmaking.html')

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
        print(data)

        # Process the data as needed (e.g., save to a database, validate, etc.)

        return jsonify({'message': 'Form submitted successfully!', 'data': data}), 200
    else:
        return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 415

if __name__ == '__main__':
    app.run(debug=True)