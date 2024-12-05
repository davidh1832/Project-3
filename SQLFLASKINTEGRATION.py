from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from typing import Optional, cast, List, Tuple

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'todolistapp'
}

currentuser = 'Billy'
currentlist = 'First'

def connect_to_database(db_config) -> Optional[MySQLConnection]:
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(db_config)
        if connection.is_connected():
            print("Connection to MySQL server successful!")
            print("MySQL Server version:", connection.get_server_info())
            return cast(MySQLConnection, connection)
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None

def execute_query(connection: mysql.connector.MySQLConnection, query: str, values: tuple) -> bool:
    """Execute a single SQL query."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        connection.commit()
        print("Query executed successfully.")
        return True
    except mysql.connector.errors.ProgrammingError as e:
        print(f"SQL Syntax Error: {e}")
    except mysql.connector.errors.IntegrityError as e:
        print(f"Constraint Violation: {e}")
    except Error as e:
        print(f"Unexpected Error: {e}")
    return False


#loads credentials from database
def load_credentials():
    try:

        connection = mysql.connector.MySQLConnection
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usertable")
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return {"users": users}
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return {"users": []}


#For new accounts
@app.route('/users/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')


    if not username or not password:
        return "Username and password are required.", 400

    try:

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        insert_query = "INSERT INTO UserTable (Username, Password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))  # Hashing the password is recommended.

           
        connection.commit()

        return f"User {username} registered successfully.", 201
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Failed to register user.", 500
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def Del_task(task_id):
    taskid = task_id
    insert_statement = "DELETE FROM taskstable WHERE taskid = %s"  
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)
        cursor.execute(insert_statement, (taskid,))
        if cursor.rowcount > 0:
            connection.commit()
            return(f"task deleted successfully.")
        else:
            return(f"Failed to delete task: {e}")
    except Exception as e:
        return(f"Failed to delete task: {e}")




#Return all users and passwords in database
@app.route('/users', methods=['GET'])
def get_users():
    # Connect to the database
    connection = mysql.connector.MySQLConnection
    cursor = connection.cursor(buffered=True)
    # Query the database
    cursor.execute("SELECT * FROM usernames")
    users = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    
    return jsonify(users)


#Login 
@app.route('/users/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        # Query the database for the user
        query = "SELECT * FROM usertable WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        # Close the connection
        cursor.close()
        connection.close()

        if user:
            currentuser = username
            return jsonify({"message": "Login successful"}), 200
            
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": "Internal server error"}), 500
    
    

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "INSERT INTO usernames (Username, Password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))

        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        return jsonify({"message": "User added successfully"}), 201
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": "Failed to add user"}), 500

@app.route('/add_list', methods=['POST'])
def create_list():
    """Add a new list and associate it with a user."""
    username = request.form.get('username')
    listname = request.form.get('listname')

    if not username or not listname:
        return "Username and list name are required", 400
    

    try:

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        list_query = "INSERT INTO todolisttable (listname) VALUES (%s)"
        cursor.execute(list_query, (listname,))
        query2= "SELECT listid FROM todolisttable where listname = %s"
        cursor.execute(query2, (listname, ))
        result = cursor.fetchone()
        for x in result:
            lid = (x)

        relation_query = "INSERT INTO userlistrelationtable (username, listid) VALUES (%s, %s)"
        cursor.execute(relation_query, (username, lid))

        connection.commit()
        connection.close()

        return "List and user association added successfully", 201
    except mysql.connector.Error as err:
        print(f"Error adding new list: {err}")
        connection.rollback()
        return "Failed to add list", 500
    
@app.route('/lists/<string:username>', methods=['GET'])
def get_lists(username):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(buffered=True)
    query = "SELECT l.listname FROM userlistrelationtable ul JOIN todolisttable l ON ul.listid = l.listid WHERE ul.username = %s"
    cursor.execute(query,(username, ))
    lists = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(lists)    
    
@app.route('/lists/<string:username>/<string:list_name>', methods=['GET'])
def get_tasks(username,list_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(buffered=True)
    query = "SELECT t.description, t.status FROM userlistrelationtable ul JOIN todolisttable l ON ul.listid = l.listid JOIN taskstable t ON l.listid = t.listid WHERE ul.username = %s AND l.listname = %s;"
    cursor.execute(query,(username,list_name,))
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(tasks)  
    
@app.route('/tasks/<string:username>/<string:list_name>', methods=['POST'])
def add_task(username, list_name):
    """Add a task to a specific list for a user."""
    task_description = request.form.get('task')

    # Validate input
    if not task_description:
        return "Task description is required.", 400

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        # Check if the user and list exist
        check_query = """SELECT l.listid FROM userlistrelationtable ul JOIN todolisttable l ON ul.listid = l.listid WHERE ul.username = %s AND l.listname = %s"""
        cursor.execute(check_query, (username, list_name))
        result = cursor.fetchone()
        for x in result:
            lid = (x)

        if not result:
            return "List not found for the specified user.", 404

         # Add the task
        insert_query = """    INSERT INTO taskstable (listid, Description, Status) VALUES (%s, %s, %s)"""
        cursor.execute(insert_query, (lid, task_description, "In Progress"))

        # Commit the transaction
        connection.commit()

        # Retrieve the inserted task for confirmation
        task_id = cursor.lastrowid
        select_query = "SELECT * FROM taskstable WHERE taskid = %s"
        cursor.execute(select_query, (task_id,))
        new_task = cursor.fetchone()

        return {
            "message": "Task added successfully.",
            "task": new_task
        }, 201
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Failed to add task.", 500

@app.route('/tasks/<string:username>/<string:list_name>/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task_completion(username, list_name, task_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        check_query = """SELECT t.taskid, t.Status FROM taskstable t JOIN todolisttable l ON t.listid = l.listid JOIN userlistrelationtable ul ON l.listid = ul.listid WHERE ul.username = %s AND l.listname = %s AND t.taskid = %s"""
        cursor.execute(check_query, (username, list_name, task_id))
        task = cursor.fetchone()
        if not task:
            return "Task not found.", 404
       
        check_status_query = "SELECT Status FROM taskstable WHERE taskid = %s"
        cursor.execute(check_status_query,(task_id,))
        checkedtask = cursor.fetchone()
        for x in checkedtask:
            currentstatus = (x)
        if currentstatus == 'In Progress':
            new_status = "Done" 
            update_query = "UPDATE taskstable SET Status = %s WHERE taskid = %s"
            cursor.execute(update_query, (new_status, task_id))
            # Commit the changes
            connection.commit()
        else:
            new_status = "In Progress" 
            update_query = "UPDATE taskstable SET Status = %s WHERE taskid = %s"
            cursor.execute(update_query, (new_status, task_id))
            # Commit the changes
            connection.commit()

        return {
            "message": "Task completion status updated.",
            "task": {
                "task_id": task_id,
                "new_status": new_status
            }
        }, 200
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Failed to update task status.", 500


    

if __name__ == '__main__':
    app.run(debug=True)
    
    
