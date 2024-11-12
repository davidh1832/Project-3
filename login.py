import json
import os

def load_credentials():
    """Load user credentials from JSON file"""
    if not os.path.exists('credentials.json'):
        return {"users": []}
    
    try:
        with open('credentials.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error reading credentials file")
        return {"users": []}

def save_credentials(credentials):
    """Save user credentials to JSON file"""
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file, indent=4)

def add_credentials(username, password):
    """Add new user credentials"""
    credentials = load_credentials()
    credentials['users'].append({"username": username, "password": password})
    save_credentials(credentials)

def remove_credentials(username, password):
    """Remove user credentials"""
    credentials = load_credentials()
    credentials['users'] = [user for user in credentials['users'] if user['username'] != username and user['password'] != password]
    save_credentials(credentials)

def verify_login(username, password):
    """Verify user login credentials"""
    credentials = load_credentials()
    
    for user in credentials['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False
