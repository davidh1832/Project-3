# api.py
import json
import os
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS for all routes

currentfile = "tasks.json"

# Load tasks from file with error handling
def load_tasks():
    try:
        with open(currentfile, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty structure if file not found or corrupted
        return {}

# Save tasks atomically to avoid data corruption
def save_tasks():
    tmp_file = f"{currentfile}.tmp"
    with open(tmp_file, "w") as file:
        json.dump(TODOS, file, indent=4)
    os.replace(tmp_file, currentfile)

# Initialize the TODOS dictionary
TODOS = load_tasks()

# Helper functions
def abort(username, list_name, todo_id):
    if username not in TODOS or list_name not in TODOS[username] or str(todo_id) not in TODOS[username][list_name]:
        abort(404, message=f"Task '{todo_id}' doesn't exist in list '{list_name}' for user '{username}'")

parser = reqparse.RequestParser()
parser.add_argument('task', location='form')
parser.add_argument('completed', type=bool, location='form')

# Todo Resource
class Todo(Resource):
    def get(self, username, list_name, todo_id):
        abort(username, list_name, todo_id)
        return TODOS[username][list_name][str(todo_id)]

    def delete(self, username, list_name, todo_id):
        abort(username, list_name, todo_id)
        del TODOS[username][list_name][str(todo_id)]
        save_tasks()
        return '', 204

    def put(self, username, list_name, todo_id):
        args = parser.parse_args()
        task = {
            'task': args['task'],
            'completed': args.get('completed', TODOS[username][list_name][str(todo_id)].get('completed', False))
        }
        TODOS[username][list_name][str(todo_id)] = task
        save_tasks()
        return task, 200
    
class Lists(Resource):
    def get(self, username):
        if username not in TODOS:
            abort(404, message=f"Lists for '{username}' not found ")
        return TODOS[username]


# Toggle task completion status
@app.route('/todos/<string:username>/<string:list_name>/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_complete(username, list_name, todo_id):
    todo_id = str(todo_id)
    abort(username, list_name, todo_id)
    TODOS[username][list_name][todo_id]['completed'] = not TODOS[username][list_name][todo_id].get('completed', False)
    save_tasks()
    return jsonify(TODOS[username][list_name][todo_id])

# TodoList Resource
class TodoList(Resource):
    def get(self, username, list_name):
        if username not in TODOS or list_name not in TODOS[username]:
            abort(404, message=f"List '{list_name}' not found for user '{username}'")
        return TODOS[username][list_name]

    def post(self, username, list_name):
        args = parser.parse_args()
        if username not in TODOS:
            TODOS[username] = {}
        if list_name not in TODOS[username]:
            TODOS[username][list_name] = {}
        
        todo_id = str(int(max(TODOS[username][list_name].keys(), default="0")) + 1)
        TODOS[username][list_name][todo_id] = {
            'task': args['task'],
            'completed': False
        }
        save_tasks()
        return TODOS[username][list_name][todo_id], 201

# API resource routing
api.add_resource(TodoList, '/todos/<string:username>/<string:list_name>')
api.add_resource(Todo, '/todos/<string:username>/<string:list_name>/<int:todo_id>')
api.add_resource(Lists,'/todos/<string:username>')


if __name__ == '__main__':
    app.run(debug=True)
