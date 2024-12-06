from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

# File paths
tasks_file = "tasks.json"
credentials_file = "credentials.json"

# Helper functions to load and save tasks
def load_tasks():
    try:
        with open(tasks_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_credentials():
    try:
        with open(credentials_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_tasks(tasks):
    tmp_file = f"{tasks_file}.tmp"
    with open(tmp_file, "w") as file:
        json.dump(tasks, file, indent=4)
    os.replace(tmp_file, tasks_file)

def save_credentials(credentials):
    tmp_file = f"{credentials_file}.tmp"
    with open(tmp_file, "w") as file:
        json.dump(credentials, file, indent=4)
    os.replace(tmp_file, credentials_file)

# Load data
tasks_data = load_tasks()
credentials_data = load_credentials()

# Route: Register User
@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    if username in credentials_data:
        return jsonify({"message": "User already exists."}), 400

    # Save password to credentials.json
    credentials_data[username] = {"password": password}
    save_credentials(credentials_data)

    # Initialize user tasks in tasks.json
    tasks_data[username] = {}
    save_tasks(tasks_data)

    return jsonify({"message": f"User {username} registered successfully."}), 201

# Route: Login User
@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    user_credentials = credentials_data.get(username)

    if not user_credentials:
        return jsonify({"message": "User does not exist."}), 404

    # Check password
    if user_credentials.get("password") != password:
        return jsonify({"message": "Invalid password."}), 401

    return jsonify({"message": "Login successful."}), 200
 

# Route: Get All Task Lists
@app.route('/lists/<string:username>', methods=['GET'])
def get_lists(username):
    if username not in TODOS:
        return jsonify({"message": "User not found."}), 404
    lists = [{"list_name": list_name} for list_name in TODOS[username].keys()]
    return jsonify(lists), 200


# Route: Create a New List
@app.route('/lists/<string:username>', methods=['POST'])
def create_list(username):
    data = request.json
    list_name = data.get('list_name')
    if username not in TODOS:
        return jsonify({"message": "User not found."}), 404
    if list_name in TODOS[username]:
        return jsonify({"message": "List already exists."}), 400
    TODOS[username][list_name] = {}
    save_tasks(TODOS)
    return jsonify({"message": f"List '{list_name}' created successfully."}), 201

# Route: Get All Tasks in a List
@app.route('/lists/<string:username>/<string:list_name>', methods=['GET'])
def get_tasks(username, list_name):
    if username not in TODOS or list_name not in TODOS[username]:
        return jsonify({"message": "List not found."}), 404
    tasks = [{"id": task_id, **task_details} for task_id, task_details in TODOS[username][list_name].items()]
    return jsonify(tasks), 200

# Route: Add a Task
@app.route('/tasks/<string:username>/<string:list_name>', methods=['POST'])
def add_task(username, list_name):
    data = request.json
    task = data.get('task')
    if username not in TODOS or list_name not in TODOS[username]:
        return jsonify({"message": "List not found."}), 404
    task_id = str(len(TODOS[username][list_name]) + 1)
    TODOS[username][list_name][task_id] = {"task": task, "completed": False}
    save_tasks(TODOS)
    return jsonify({"message": "Task added successfully.", "task": TODOS[username][list_name][task_id]}), 201

# Route: Toggle Task Completion Status
@app.route('/tasks/<string:username>/<string:list_name>/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task_completion(username, list_name, task_id):
    task_id = str(task_id)

    # Check if user and task exist
    if username not in tasks_data or list_name not in tasks_data[username] or task_id not in tasks_data[username][list_name]:
        return jsonify({"message": "Task not found."}), 404

    task = tasks_data[username][list_name][task_id]
    task['completed'] = not task['completed']  # Toggle the 'completed' status

    save_tasks(tasks_data)

    return jsonify({
        "message": "Task completion status updated.",
        "task": task
    }), 200


# Route: Delete a Task
@app.route('/tasks/<string:username>/<string:list_name>/<string:task_id>', methods=['DELETE'])
def delete_task(username, list_name, task_id):
    if username not in TODOS or list_name not in TODOS[username] or task_id not in TODOS[username][list_name]:
        return jsonify({"message": "Task not found."}), 404
    del TODOS[username][list_name][task_id]
    save_tasks(TODOS)
    return jsonify({"message": "Task deleted successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)

