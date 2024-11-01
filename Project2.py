import json
import os
from colorama import Fore, Style, init
from dotenv import load_dotenv

load_dotenv('Secrets.env')

secret = os.getenv("PASS_KEY")
current_user = ""
current_list = ""

# Load user data from file
def load_user_data(user):
    user_file = f"{user}_data.json"
    try:
        with open(user_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to file
def save_user_data(user, data):
    user_file = f"{user}_data.json"
    with open(user_file, "w") as file:
        json.dump(data, file, indent=4)

# Password verification
def verify_password(stored_password):
    attempts = 3
    while attempts > 0:
        password = input("Enter the password: ")
        if password == stored_password:
            print("Access granted!")
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. You have {attempts} attempt(s) left.")
    print("Access denied!")
    return False

# Select or create a user
def select_user():
    global current_user, current_list
    current_user = input("Enter your username: ")
    user_data = load_user_data(current_user)
    
    if not user_data:
        print(Fore.GREEN + f"User '{current_user}' created.")
        save_user_data(current_user, {"lists": {}})
    else:
        print(Fore.GREEN + f"Welcome back, {current_user}!")

    current_list = select_list(user_data)
    return user_data

# Select or create a to-do list for the current user
def select_list(user_data):
    if "lists" not in user_data:
        user_data["lists"] = {}

    if user_data["lists"]:
        print("\nAvailable lists:")
        for index, list_name in enumerate(user_data["lists"].keys()):
            print(f"{index + 1}. {list_name}")

        list_choice = input("Enter the list number to use or type 'new' to create a new list: ")
        if list_choice.lower() == 'new':
            new_list_name = input("Enter a name for your new list: ")
            user_data["lists"][new_list_name] = []
            save_user_data(current_user, user_data)
            return new_list_name
        else:
            try:
                list_index = int(list_choice) - 1
                list_name = list(user_data["lists"].keys())[list_index]
                print(Fore.GREEN + f"List '{list_name}' selected.")
                return list_name
            except (ValueError, IndexError):
                print("Invalid choice.")
                return select_list(user_data)
    else:
        new_list_name = input("No lists found. Enter a name for your new list: ")
        user_data["lists"][new_list_name] = []
        save_user_data(current_user, user_data)
        return new_list_name

# Add a task to the current list
def add_task(user_data):
    task = input("Enter the task: ")
    user_data["lists"][current_list].append({"task": task, "status": "Incomplete"})
    print(Fore.GREEN + "Task added!")
    save_user_data(current_user, user_data)

# Show all tasks in the current list
def show_tasks(user_data):
    tasks = user_data["lists"].get(current_list, [])
    if tasks:
        print(Style.BRIGHT + f"\nTasks in '{current_list}':")
        for index, task in enumerate(tasks):
            currentStatus = task["status"]
            status = Fore.GREEN + "Done" if currentStatus == "Complete" else Fore.YELLOW + "In Progress" if currentStatus == "InProgress" else Fore.RED + "Incomplete"
            print(f"{index + 1}. {task['task']} - {status}")
    elif select_list(user_data):
        print(Style.BRIGHT + f"\nTasks in '{new_list_name}':")
    else:
        print(Fore.YELLOW + "No tasks to show.")

# Update task status in the current list
def update_task_status(user_data):
    tasks = user_data["lists"].get(current_list, [])
    if tasks:
        try:
            task_index = int(input(Style.BRIGHT + "Enter the task # you want to update: ")) - 1
            if 0 <= task_index < len(tasks):
                print(Fore.GREEN + "1. Complete")
                print(Fore.YELLOW + "2. In Progress")
                print(Fore.RED + "3. Incomplete")
                newStatus = int(input("Enter the status number: "))
                
                if newStatus == 1:
                    tasks[task_index]["status"] = "Complete"
                elif newStatus == 2:
                    tasks[task_index]["status"] = "In Progress"
                elif newStatus == 3:
                    tasks[task_index]["status"] = "Incomplete"
                else:
                    print("Invalid choice.")
                    return

                print(Fore.GREEN + f"Task '{tasks[task_index]['task']}' marked as {tasks[task_index]['status']}.")
                save_user_data(current_user, user_data)
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")
    else:
        print("No tasks available to update.")

# Delete a task in the current list
def delete_task(user_data):
    tasks = user_data["lists"].get(current_list, [])
    if tasks:
        try:
            del_input = input("Enter the task number to delete (or type 'all' to clear all tasks): ")
            if del_input.lower() == "all":
                user_data["lists"][current_list] = []
                print(Fore.GREEN + "All tasks cleared!")
            else:
                task_index = int(del_input) - 1
                if 0 <= task_index < len(tasks):
                    deleted_task = tasks.pop(task_index)
                    print(Fore.GREEN + f"Task '{deleted_task['task']}' deleted!")
                else:
                    print("Invalid task number.")
            save_user_data(current_user, user_data)
        except ValueError:
            print("Please enter a valid task number.")
    else:
        print("No tasks to delete.")

def edit_task(tasks):
    if tasks:
        try:
            task_index = int(input("Enter the task number to edit: ")) - 1
            if 0 <= task_index < len(tasks):
                new_task = input(f"Enter the new task description for Task {task_index + 1}: ")
                tasks[task_index]["task"] = new_task
                print(f"Task {task_index + 1} has been updated.")
                save_tasks(tasks)
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")
    else:
        print("No tasks to edit.")

# Main function
def main():
    if verify_password(secret):
        user_data = select_user()
        init(autoreset=True)
        os.system('cls' if os.name == 'nt' else 'clear')

        while True:
            print(Style.BRIGHT + "\n===== To-Do List =====")
            print("1. Add Task")
            print("2. Show Tasks")
            print("3. Delete Task")
            print("4. Edit Task")
            print("5. Change Task Status")
            print("6. Switch List")
            print("7. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                add_task(user_data)
            elif choice == '2':
                show_tasks(user_data)
            elif choice == '3':
                delete_task(user_data)
            elif choice == '4':
                edit_task(tasks)
            elif choice == '5':
                update_task_status(user_data)
            elif choice == '6':
                current_list = select_list(user_data)  
            elif choice == '7':
                print("Exiting the To-Do List.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()