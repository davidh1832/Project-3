import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from typing import Optional, cast, List, Tuple

def connect_to_database(host: str, user: str, password: str, database: str) -> Optional[MySQLConnection]:
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
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


def new_user(username: str, hashed_password: str, connection: mysql.connector.MySQLConnection) -> bool:
    """Add a new user to the database."""
    query = "INSERT INTO UserTable (Username, Password) VALUES (%s, %s)"
    return execute_query(connection, query, (username, hashed_password))


def new_list(username: str, list_id: int, list_name: str, connection: mysql.connector.MySQLConnection) -> bool:
    """Add a new list and associate it with a user."""
    try:
        with connection.cursor() as cursor:
            # Add new list
            list_query = "INSERT INTO TodoListTable (ListName) VALUES (%s)"
            cursor.execute(list_query, (list_name,))
            
            # Associate list with the user
            relation_query = "INSERT INTO UserListRelationTable (Username, ListId) VALUES (%s, %s)"
            cursor.execute(relation_query, (username, list_id))
        
        connection.commit()
        print("List and user association added successfully.")
        return True
    except Error as e:
        print(f"Error adding new list: {e}")
        connection.rollback()
    return False


def new_task(list_id: int, description: str, completion_date: str, connection: mysql.connector.MySQLConnection) -> bool:
    """Add a new task to the database."""
    query = """INSERT INTO TasksTable (EstimatedCompletionDate, Description, Status) 
               VALUES (%s, %s, %s)"""
    return execute_query(connection, query, (completion_date, description, "In Progress"))


def update_task(task_id: int, description: str, completion_date: str, status: str, connection: mysql.connector.MySQLConnection) -> bool:
    """Update task details in the database."""
    query = """UPDATE TasksTable 
               SET EstimatedCompletionDate = %s, Description = %s, Status = %s 
               WHERE TaskId = %s"""
    return execute_query(connection, query, (completion_date, description, status, task_id))

def get_lists(username: str, connection: MySQLConnection) -> Optional[List[Tuple]]:
    """
    Get all the ToDo lists related to the user.

    Args:
        username (str): The username of the user.
        connection (MySQLConnection): The MySQL connection object.

    Returns:
        Optional[List[Tuple]]: A list of tuples containing list names, or None if an error occurs.
    """
    query = """
        SELECT l.ListName 
        FROM UserListRelationTable ul 
        JOIN TodoListTable l ON ul.ListId = l.ListId  
        WHERE ul.Username = %s
    """
    values = (username,)

    try:
        with connection.cursor() as cursor:  # Ensure the cursor is properly closed
            cursor.execute(query, values)
            results = cursor.fetchall()  # Fetch all results as a list of tuples
        print("Query executed successfully.")
        return results
    except mysql.connector.errors.ProgrammingError as e:
        print(f"SQL Syntax Error: {e}")
    except mysql.connector.errors.IntegrityError as e:
        print(f"Constraint Violation: {e}")
    except mysql.connector.Error as e:
        print(f"Unexpected MySQL Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    return None

# Example usage
if __name__ == "__main__":
    # Database connection details
    db_host="localhost"   # e.g., "localhost" or "127.0.0.1"
    db_user="remote_user"         # MySQL username
    db_password="Simple_passsword123$"     # MySQL password
    db_name="ToDoApp" 

    # Establish connection
    conn = connect_to_database(db_host, db_user, db_password, db_name)

    if conn:
        # Add a new user
        if new_user("john_doe", "hashed_password_123", conn):
            print("New user added successfully.")
        
        # Add a new list
        if new_list("john_doe", 1, "My Todo List", conn):
            print("New list added successfully.")

        # Add a new task
        if new_task(1, "Complete Python project", "2024-12-01", conn):
            print("New task added successfully.")

        # Update an existing task
        if update_task(1, "Finalize Python project", "2024-12-02", "Completed", conn):
            print("Task updated successfully.")

        # Close the connection
        conn.close()
