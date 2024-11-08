import json
import os
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS for all routes

currentfile = "tasks.json"

def load_tasks():
    try:
        with open(currentfile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tasks():
    with open(currentfile, "w") as file:
        json.dump(TODOS, file)

TODOS = load_tasks()

def abort_if_todo_doesnt_exist(todo_id):
    if str(todo_id) not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def abort_if_empty():
    abort(404, message="Nothing in list yet. Go ahead and add a task!")

parser = reqparse.RequestParser()
parser.add_argument('task', location='form')
parser.add_argument('completed', type=bool, location='form')
parser.add_argument('file', location='form')

# Todo
class Todo(Resource):
    def get(self, todo_id=None):
        if todo_id:
            abort_if_todo_doesnt_exist(todo_id)
            return TODOS[str(todo_id)]
        
        if not TODOS:
            abort_if_empty()
        return TODOS

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[str(todo_id)]
        save_tasks()
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {
            'task': args['task'],
            'completed': args.get('completed', TODOS[str(todo_id)].get('completed', False))
        }
        TODOS[str(todo_id)] = task
        save_tasks()
        return task, 200

# Toggle completion status
@app.route('/todos/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_complete(todo_id):
    todo_id = str(todo_id)
    abort_if_todo_doesnt_exist(todo_id)
    TODOS[todo_id]['completed'] = not TODOS[todo_id].get('completed', False)
    save_tasks()
    return jsonify(TODOS[todo_id])

#ChangeList
@app.route('/todos/changelist',methods=['PATCH'])
def change_list():
    global currentfile
    global TODOS
    args = parser.parse_args()
    currentfile = args['file']
    TODOS = load_tasks()
    return currentfile

def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[str(todo_id)]
        save_tasks()
        return '', 204
# TodoList
class TodoList(Resource):
    def get(self):
        if not TODOS:
            abort_if_empty()
        return TODOS

    def post(self):
        args = parser.parse_args()
        if TODOS:
            todo_id = int(max(TODOS.keys())) + 1
        else:
            todo_id = 1
        TODOS[str(todo_id)] = {
            'task': args['task'],
            'completed': False
        }
        save_tasks()
        return TODOS[str(todo_id)], 201
    



# API resource routing
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
