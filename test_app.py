
import unittest
from app import app, TODOS, load_tasks, save_tasks

class TodoApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a test client
        cls.client = app.test_client()
        cls.client.testing = True

    def setUp(self):
        # Prepare a fresh copy of TODOS for each test to ensure independence
        TODOS.clear()
        TODOS.update({
            '1': {'task': 'Write unit tests', 'completed': False},
            '2': {'task': 'Review code', 'completed': False}
        })
        save_tasks()

    def test_get_all_todos(self):
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_single_todo(self):
        response = self.client.get('/todos/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['task'], 'Write unit tests')

    def test_get_non_existent_todo(self):
        response = self.client.get('/todos/999')
        self.assertEqual(response.status_code, 404)

    def test_create_todo(self):
        response = self.client.post('/todos', data={'task': 'New task', 'completed': False})
        self.assertEqual(response.status_code, 201)
        self.assertIn('New task', [todo['task'] for todo in TODOS.values()])

    def test_update_todo(self):
        response = self.client.put('/todos/1', data={'task': 'Updated task', 'completed': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TODOS['1']['task'], 'Updated task')
        self.assertTrue(TODOS['1']['completed'])

    def test_delete_todo(self):
        response = self.client.delete('/todos/1')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn('1', TODOS)

    def test_delete_non_existent_todo(self):
        response = self.client.delete('/todos/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
