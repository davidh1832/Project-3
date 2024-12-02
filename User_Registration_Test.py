from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load credentials from a file
def load_credentials():
    if not os.path.exists('credentials.json'):
        return {"users": []}
    try:
        with open('credentials.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"users": []}

# Save credentials to a file
def save_credentials(credentials):
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file, indent=4)

# Add a new user
@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    print(data)  # Log the received data for debugging
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    credentials = load_credentials()
    if any(user['username'] == username for user in credentials['users']):
        return jsonify({"error": "User already exists"}), 409

    credentials['users'].append({"username": username, "password": password})
    save_credentials(credentials)
    return jsonify({"message": "User added successfully"}), 201

# Remove a user
@app.route('/remove', methods=['DELETE'])
def remove_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    credentials = load_credentials()
    filtered_users = [
        user for user in credentials['users'] 
        if user['username'] != username or user['password'] != password
    ]

    if len(filtered_users) == len(credentials['users']):
        return jsonify({"error": "User not found"}), 404

    credentials['users'] = filtered_users
    save_credentials(credentials)
    return jsonify({"message": "User removed successfully"}), 200

# Verify login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    credentials = load_credentials()
    for user in credentials['users']:
        if user['username'] == username and user['password'] == password:
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(debug=True)
