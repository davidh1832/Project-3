## TO DO LIST

Repository for Software Engineering project #3 focusing on further development of a To-Do-List. This repository was created for our third group project for CS 230 Software Engineering, meant to further expand upon the To-Do-List by merging two groups with similar ideas together. The To-Do-List was implemented with the use of a restful API, using the Flask API Framework.

## Installation
Download the files and open them in whatever code editor you prefer, or use git to clone the repository.
```bash
git clone https://github.com/davidh1832/Project-3.git
```

## Usage
Python

## Functions
```python
#These are the functions from Client

add_task()
#Adds a task to the list through sending a POST request to the API

show_tasks()
#Lists all of the tasks in a list through a GET request to the API

delete_task()
#Deletes the specified task from the currently accessed list through a DELETE request to the API

edit_task()
#Edits the specified tasks name through a PUT request to the API

toggle_task()
#toggles the specified task to display completion through a PATCH request to the API

select_list()
#Changes the accesed list

show_lists()
#displays all of the lists of the user


```

## Login
The application includes a user authentication system with the following functions:

### Load user credentials from JSON file

load_credentials()
- Reads user credentials from credentials.json
- Creates empty credentials if file doesn't exist
- Returns credentials data structure

### Save user credentials to JSON file 

save_credentials()
- Writes current credentials to credentials.json
- Formats JSON with proper indentation

### Add new user credentials

add_credentials()
- Adds a new username/password pair to credentials
- Automatically saves updated credentials

### Remove user credentials

remove_credentials() 
- Removes specified username/password from credentials
- Automatically saves updated credentials

#Verify user login credentials

verify_login()
- Checks if username/password combination exists
- Returns True if valid credentials, False otherwise



## Contribution
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Current Contributors: 
  
