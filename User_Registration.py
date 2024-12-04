from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import bcrypt
import os
from login import load_credentials, save_credentials, add_credentials, remove_credentials, verify_login

app = Flask(__name__)
CORS(app)

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
    add_credentials(username, password)
    return jsonify({"message": "User added successfully"}), 201

# Remove a user
@app.route('/remove', methods=['DELETE'])
def remove_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    remove_credentials(username, password)
    return jsonify({"message": "User removed successfully"}), 200

# Verify login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if verify_login(username, password):
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# List users (optional, for debugging or admin purposes)
@app.route('/users', methods=['GET'])
def list_users():
    credentials = load_credentials()
    return jsonify({"users": credentials['users']}), 200

if __name__ == '__main__':
    app.run(debug=True)
