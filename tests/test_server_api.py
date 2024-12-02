import unittest
# from mysql.connector import MySQLConnection
# from typing import Optional
import sys
sys.path.append('.')
from server_api import (
    connect_to_database,
    new_user,
    new_list,
    new_task,
    update_task,
    get_lists,
)

class TestDatabaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test database connection."""
        cls.connection = connect_to_database(
            host="localhost",   # e.g., "localhost" or "127.0.0.1"
            user="remote_user",         # MySQL username
            password="Simple_passsword123$",     # MySQL password
            database="ToDoApp", 
        )
        if not cls.connection:
            raise RuntimeError("Failed to connect to the test database.")

    @classmethod
    def tearDownClass(cls):
        """Close the database connection."""
        if cls.connection and cls.connection.is_connected():
            cls.connection.close()

    # def setUp(self):
    #     """Clean up database and set initial state."""
    #     with self.connection.cursor() as cursor:
    #         # Reset test tables
    #         cursor.execute("DELETE FROM TasksTable")
    #         cursor.execute("DELETE FROM UserListRelationTable")
    #         cursor.execute("DELETE FROM TodoListTable")
    #         cursor.execute("DELETE FROM UserTable")
    #     self.connection.commit()

    def test_new_user(self):
        """Test adding a new user."""
        result = new_user("test_user", "hashed_password", self.connection)
        self.assertTrue(result)

        # Verify user was added
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM UserTable WHERE Username = %s", ("test_user",))
            user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[0], "test_user")  # Check username
        self.assertEqual(user[1], "hashed_password")  # Check password

    def test_new_list(self):
        """Test adding a new list and associating it with a user."""
        new_user("test_user", "h" * 255, self.connection)
        result = new_list("test_user", 1, "Test List", self.connection)
        self.assertTrue(result)

        # Verify list was added
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM TodoListTable WHERE ListName = %s", ("Test List",))
            list_entry = cursor.fetchone()
        self.assertIsNotNone(list_entry)
        self.assertEqual(list_entry[1], "Test List")  # Check list name

    def test_new_task(self):
        """Test adding a new task."""
        result = new_task(1, "Test Task", "2024-12-31", self.connection)
        self.assertTrue(result)

        # Verify task was added
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM TasksTable WHERE Description = %s", ("Test Task",))
            task = cursor.fetchone()
        self.assertIsNotNone(task)
        self.assertEqual(task[2], "Test Task")  # Check description

    def test_update_task(self):
        """Test updating a task."""
        new_task(1, "Test Task", "2024-12-31", self.connection)
        result = update_task(1, "Updated Task", "2024-12-25", "Completed", self.connection)
        self.assertTrue(result)

        # Verify task was updated
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM TasksTable WHERE TaskId = %s", (1,))
            task = cursor.fetchone()
        self.assertIsNotNone(task)
        self.assertEqual(task[2], "Updated Task")  # Check updated description
        self.assertEqual(task[3], "2024-12-25")  # Check updated date
        self.assertEqual(task[4], "Completed")  # Check updated status

    def test_get_lists(self):
        """Test retrieving lists for a user."""
        new_user("test_user", "hashed_password", self.connection)
        new_list("test_user", 1, "Test List", self.connection)

        lists = get_lists("test_user", self.connection)
        self.assertIsNotNone(lists)
        self.assertEqual(len(lists), 1)
        self.assertEqual(lists[0][0], "Test List")  # Verify list name


if __name__ == "__main__":
    unittest.main()
