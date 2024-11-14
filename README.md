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
#Load tasks into Json file

load_tasks()

#Save tasks to Json file

save_Tasks()

#Clear all the tasks from the Json file

clear_Tasks()

#Add a task into the Json file

add_Task()

#Displays tasks written in the Json file

show_Tasks()

#Changes the status of a task(Complete, Incomplete, Inprogress, etc)

update_task_status()

#deletes a task from the Json file

delete_task()

#Access a certain task and make changes to it

edit_task()

#Verifies the password defined in the user's environmental variable file.

verify_password()

#Creates a JSON file to act as another to-do list

add_list()

#changes which profile is used to access a different to-do list

select_user()

# Select or create a to-do list for the current user
select_list()
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
  
