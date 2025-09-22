#todo list
"""
- add, update and delete tasks
- mark a task as in progress or done
- list tasks
- list done tasks
- list not done tasks
- list in progress tasks
- use positional arguments
- use a JSON file to store tasks
- create a JSON file if one does not exists
- do not use external frameworks or libraries
- handle errors gracefully

properties

 - id
 - description
 - status(todo, in-progress, done)
 - createdAt
 - updatedAt
"""
import json
import os
import datetime


#creating a JSON file in case there is none
filename = "tasks.json"

if not os.path.exists(filename):
    print("No JSON file found. Creating a new one...")

    default_data = {
        "tasks": []
    }
    with open(filename, "w") as file:
        json.dump(default_data, file, indent=4)

#------------------------------------------------#

#function to add tasks to JSON file
def add_task(name, description, status, createdAt, updatedAt):

    print("\nPreparing to add a new task...\n")

    #opening JSON file to add task
    with open(filename, "r") as file:
        data = json.load(file)

        #id counter that checks other id's to make a new higher one
        if data["tasks"]:
            counter = max(task["id"] for task in data["tasks"]) + 1
        else:
            counter = 1

        #dictionarie with parameters to send to JSON file
        new_task = {
            "id":counter,
            "name":name,
            "description":description,
            "status":status,
            "createdAt":createdAt,
            "updatedAt":updatedAt
        }

        #appending the new task to JSON file
        data["tasks"].append(new_task)

        #overwiriting existing data with new updated one
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("\nTask added successfully!\n")

#------------------------------------------------#

#function to delete tasks from JSON file
def delete_task():
    
    print("\nPreaparing to delete a task...\n")

    #opening JSON file to delete a task
    with open(filename, "r") as file:
        data = json.load(file)

        #printing the list so you can see the tasks to erase
        print(json.dumps(data["tasks"], indent=4))

        #choose a task by ID to remove
        try:
            remove = int(input("Choose the ID of the task you want to delete: "))
        except ValueError:
            print("\nInvalid input. You should type a number.\n")
            return

        #removes selected task
        data["tasks"] = [task for task in data["tasks"] if task ["id"] != remove]
    
    #overwrites JSON data now without chosen task
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("\nTask deleted successfully!\n")

#------------------------------------------------#

#function to update tasks from JSON file
def update_task():
    
    print("\nPreparing to update a task...\n")

    #opening JSON file to update a task
    with open(filename, "r") as file:
        data = json.load(file)

    #print all tasks so user can choose one to update    
    print(json.dumps(data["tasks"], indent=4))

    #asks for choosen task ID (also handles input errors)
    try:
        update = int(input("Choose the ID of a task to update: "))
    except ValueError:
        print("\nInvalid input. Enter a number.\n")
        return
    
    #searches task by task to find one that matches the required ID (also handles if task doesn't exist)
    task = next((t for t in data["tasks"] if t["id"] == update), None)

    if not task:
        print("\nTask not found\n")
        return
    
    #asks for all parameters to change
    print("\nLeave empty to keep current value\n")
    new_name = input(f"New name (Current: {task['name']}): ") or task["name"]
    new_description = input(f"New description (Current: {task['description']}): ") or task["description"]

    verify_status = ("todo", "in-progress", "done")
    while True:
        new_status = input(f"New status (Current: {task['status']}): ").lower() or task["status"]
        if new_status in verify_status:
            break
        else:
            print("\nInvalid status. Choose between 'todo', 'in-progress' or 'done'\n")

    #changes all parameters accordingly
    task["name"] = new_name
    task["description"] = new_description
    task["status"] = new_status
    task["updatedAt"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    #overwrites all changes into JSON file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("\nTask updated successfully!\n")

#------------------------------------------------#

#function to list all tasks in the JSON file
def list_tasks(filter_status=None):

    #opening JSON file to print
    with open(filename, "r") as file:
        data = json.load(file)

    if not data["tasks"]:
        print("\nNo tasks found\n")
        return
    
    
    tasks = data["tasks"]

    
    if filter_status:
        verify_status = ("todo", "in-progress", "done")
        if filter_status.lower() in verify_status:
            tasks = [task for task in tasks if task["status"].lower() == filter_status.lower()]
            if tasks == []:
                print("No tasks found with the designed status.")
                return
        else:
            print("\nInvalid status. Choose between 'todo' or 'in-progress'\n")
            return
    
    print(json.dumps(tasks, indent=4))

#------------------------------------------------#

while True:
        start = input("What do you want to do? (Enter 'help' for a list of commands) ")

        if start == "help":
            print("""\nList  of all commands:
                
                'add' -> add a task to the list
                'del' -> delete a task from the list
                'upt' -> update a task from the list
                'ls' -> list all tasks
                'esc' -> exit program\n""")
            
            
        elif start == "add":
            
            name = input("Write the name of your task(Type 'esc' to cancel): ")
            if name.lower() == "esc":
                print("Returning...\n")
                continue
            else:
                description = input("Write a description for your task: ")

            verify_status = ("todo", "in-progress")
            while True:
                status = input("What is the status of the task? (todo, in-progress) ").lower()
                if status in verify_status:
                    break
                else:
                    print("\nInvalid status. Choose between 'todo' or 'in-progress'\n")

            createdAt = datetime.datetime.now()
            FcreatedAt = createdAt.strftime("%d-%m-%Y %H:%M")
            updatedAt = datetime.datetime.now()
            FupdatedAt = updatedAt.strftime("%d-%m-%Y %H:%M")

            add_task(name, description, status, FcreatedAt, FupdatedAt)


        elif start == "del":
            delete_task()


        elif start == "upt":
            update_task()


        elif start == "ls":
            print(f"\n Leave clear to show all.\n")
            choice = input("What do you want to list? ('todo','in-progress',done,) ")
            list_tasks(choice)


        elif start == "esc":
            break


        else:
            print("Invalid input. Type 'help' for a list of all usable commands.")
            continue