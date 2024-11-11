import unittest
import os
import json
from login import load_credentials, save_credentials, add_credentials, remove_credentials, verify_login

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up test cases - create test credentials file"""
        self.test_credentials = {
            "users": [
                {
                    "username": "testuser",
                    "password": "testpass"
                }
            ]
        }
        save_credentials(self.test_credentials)

    def tearDown(self):
        """Clean up after tests - remove test credentials file"""
        if os.path.exists('credentials.json'):
            os.remove('credentials.json')

    def test_load_credentials(self):
        """Test loading credentials from file"""
        credentials = load_credentials()
        self.assertEqual(credentials, self.test_credentials)

    def test_load_credentials_no_file(self):
        """Test loading credentials when file doesn't exist"""
        if os.path.exists('credentials.json'):
            os.remove('credentials.json')
        credentials = load_credentials()
        self.assertEqual(credentials, {"users": []})

    def test_add_credentials(self):
        """Test adding new user credentials"""
        add_credentials("newuser", "newpass")
        credentials = load_credentials()
        self.assertTrue(
            {"username": "newuser", "password": "newpass"} in credentials["users"]
        )

    def test_remove_credentials(self):
        """Test removing user credentials"""
        remove_credentials("testuser", "testpass")
        credentials = load_credentials()
        self.assertFalse(
            {"username": "testuser", "password": "testpass"} in credentials["users"]
        )

    def test_verify_login_success(self):
        """Test successful login verification"""
        self.assertTrue(verify_login("testuser", "testpass"))

    def test_verify_login_failure(self):
        """Test failed login verification"""
        self.assertFalse(verify_login("wronguser", "wrongpass"))

if __name__ == '__main__':
    unittest.main() 