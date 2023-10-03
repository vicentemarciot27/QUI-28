from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Handle CORS

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print(data)  # Log received data to the console
    return jsonify({"message": "Data received successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
