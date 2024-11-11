# client.py
import requests

BASE_URL = "http://127.0.0.1:5000/todos"

def select_user():
    return input("Enter your username: ")

def select_list():
    return input("Enter the list name: ")

def show_tasks(username, list_name):
    url = f"{BASE_URL}/{username}/{list_name}"
    response = requests.get(url)
    if response.status_code == 404:
        print("List not found.")
    else:
        tasks = response.json()
        for task_id, task_data in tasks.items():
            status = "✓" if task_data['completed'] else "✗"
            print(f"{task_id}. {task_data['task']} [{status}]")

def add_task(username, list_name):
    task = input("Enter the new task: ")
    url = f"{BASE_URL}/{username}/{list_name}"
    response = requests.post(url, data={'task': task})
    if response.status_code == 201:
        print("Task added successfully.")
    else:
        print("Failed to add task.")

def delete_task(username, list_name):
    task_id = input("Enter the task ID to delete: ")
    url = f"{BASE_URL}/{username}/{list_name}/{task_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print("Task deleted successfully.")
    else:
        print("Failed to delete task.")

def toggle_task(username, list_name):
    task_id = input("Enter the task ID to toggle completion: ")
    url = f"{BASE_URL}/{username}/{list_name}/{task_id}/toggle"
    response = requests.patch(url)
    if response.status_code == 200:
        print("Task completion toggled.")
    else:
        print("Failed to toggle task completion.")

def main():
    username = select_user()
    list_name = select_list()

    while True:
        print("\n1. Show Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Toggle Task Completion")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks(username, list_name)
        elif choice == '2':
            add_task(username, list_name)
        elif choice == '3':
            delete_task(username, list_name)
        elif choice == '4':
            toggle_task(username, list_name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
