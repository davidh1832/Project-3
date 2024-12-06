## TO DO LIST

Repository for Software Engineering final project focusing on further development of a To-Do-List. This repository was created for our third group project for CS 230 Software Engineering, meant to further expand upon the To-Do-List by merging two groups with similar ideas together. The To-Do-List was implemented with the use of a restful API, using the Flask API Framework. Two teams were used for this project sprint, a front end and a back end team. The front end team spent time enhancing UI in the form of a GUI using ReTool. The backend team spent development time further enhancing security of user profiles as well as making the leap from JSON file storage to a database, created and managed through MySQL.

## Installation
Download the files and open them in whatever code editor you prefer, or use git to clone the repository.
```bash
git clone https://github.com/davidh1832/Project-3.git
```

## Usage
Python
MySQL
ReTool

## Functions
```python
#These are the functions from Client

add_task()
#Adds a task to the list through sending a POST request to the API

show_tasks()
#Lists all of the tasks in a list through a GET request to the API

delete_task()
#Deletes the specified task from the currently accessed list through a DELETE request to the API
add_list()
# allows a user to add a new list to their profile

toggle_task()
#toggles the specified task to display completion through a PATCH request to the API

select_list()
#Changes the accesed list

show_lists()
#displays all of the lists of the user


```
```MySQL
Tasks Table
-Stores all user tasks
-unique ID for each task
-Status, Task description and ID are stored information

ToDoListTable
-Stores lists and lists ID for linking with users

UserTable
-Stores username and user password for verification

UserListRelationTable
-Links username to avaliable list IDs.
```


## Login
The application includes a user authentication system with the following functions:

### Load user credentials from Database

load_credentials()
- Reads user credentials from user table in database
- Returns credentials data structure


### Save user credentials to database 

save_credentials()
- Writes current credentials to credentials.json
- Formats JSON with proper indentation

Register_User()
- Cretes a user profile in database
- verifies username has not been already saved to database



### Remove user credentials

remove_credentials() 
- Removes specified username/password from credentials
- Automatically saves updated credentials
- admin level function

#Verify user login credentials

verify_login()
- Checks if username/password combination exists
- Returns True if valid credentials, False otherwise



## Contribution
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Current Contributors: 
  
