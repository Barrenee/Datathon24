from flask import Flask, render_template, session, jsonify, request, send_file

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/matchmaking')
def matchmaking():
    return render_template('matchmaking.html')

if __name__ == '__main__':
    app.run()