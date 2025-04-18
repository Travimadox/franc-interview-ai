#!/usr/bin/env python3
"""
Task Tracker Application

A simple console application for tracking tasks.
"""
import json
import os
from datetime import datetime
import time
import uuid
import datetime

# Global variables
TASKS_FILE = "tasks.json"
tasks = {}

def load_tasks():
    """Load tasks from the JSON file."""
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                tasks = json.load(f)
        except json.JSONDecodeError as e:
            # Bug: Silent failure on corrupted JSON, doesn't initialize 'tasks'
            print(f"Warning: Tasks file is corrupted. The error is {e}")

            # Missing: Should initialize tasks = {} here
            tasks = {}
    else:
        # Create an empty JSON file if it doesn't exist
        save_tasks()

def save_tasks():
    """Save tasks to the JSON file."""
    # Bug: No error handling for file operations
    try:
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def generate_task_id():
    """Generate a new unique task ID."""
    # Bug: This doesn't guarantee uniqueness if tasks are deleted
    #if not tasks:
        #return 1
    #return max(int(task_id) for task_id in tasks.keys()) + 1
    # Using UUID for unique task ID
    return str(uuid.uuid4())

def add_task():
    """Add a new task."""
    print("\n=== Add New Task ===")
    
    title = input("Enter task title: ")
    # Bug: Missing validation for empty title
    if not title:       
        print("Title cannot be empty.")
        return  
    
    description = input("Enter task description: ")
    # Bug: Missing validation for empty description
    if not description:
        print("Description cannot be empty.")
        return
    
    # Bug: No validation or error handling for date format
    due_date = input("Enter due date (YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Missing: No validation that the date is in the future
    if datetime.datetime.strptime(due_date, "%Y-%m-%d") < datetime.datetime.now():
        print("Due date cannot be in the past.")
        return
    
    task_id = str(generate_task_id())
    tasks[task_id] = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "incomplete",
        # Bug: Missing created_date field required by specs
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    save_tasks()
    print(f"Task {task_id} added successfully!")

def view_all_tasks():
    """View all tasks."""
    print("\n=== All Tasks ===")
    
    if not tasks:
        print("No tasks found.")
        return
    
    # Bug: This doesn't format output nicely with proper spacing
    #print("ID | Title | Due Date | Status")
    #print("-" * 40)
    #for task_id, task in tasks.items():
    #   print(f"{task_id} | {task['title']} | {task['due_date']} | {task['status']}")

    print(f"{'ID':<5} {'Title':<20} {'Due Date':<15} {'Status':<10}")
    print("-" * 50)
    for task_id, task in tasks.items():
        print(f"{task_id:<5} {task['title']:<20} {task['due_date']:<15} {task['status']:<10}")

def view_task():
    """View details of a specific task."""
    print("\n=== View Task ===")
    
    task_id = input("Enter task ID: ")
    
    # Bug: Missing validation for non-existent task IDs
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    task = tasks[task_id]
    print(f"ID: {task_id}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Status: {task['status']}")

def update_task():
    """Update an existing task."""
    print("\n=== Update Task ===")
    
    task_id = input("Enter task ID: ")
    
    # Bug: Missing validation for non-existent task IDs
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    task = tasks[task_id]
    
    print("Leave field empty to keep current value.")
    print(f"Current Title: {task['title']}")
    new_title = input("New Title: ")
    
    print(f"Current Description: {task['description']}")
    new_description = input("New Description: ")
    
    print(f"Current Due Date: {task['due_date']}")
    new_due_date = input("New Due Date (YYYY-MM-DD): ")
    
    # Bug: No validation on due date format
    try:
        if new_due_date:
            datetime.datetime.strptime(new_due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Bug: No validation that the date is in the future
    if new_due_date and datetime.datetime.strptime(new_due_date, "%Y-%m-%d") < datetime.datetime.now():
        print("Due date cannot be in the past.")
        return
    
    # Update task with new values, keeping old values if input is empty
    if new_title:
        task['title'] = new_title
    if new_description:
        task['description'] = new_description
    if new_due_date:
        # Bug: No validation of date format
        task['due_date'] = new_due_date
    
    save_tasks()
    print(f"Task {task_id} updated successfully!")

# Bug: Missing implementation of mark_task_complete function (FR1.7)
def mark_task_complete():
    """Mark a task as complete."""
    print("\n=== Mark Task Complete ===")
    
    task_id = input("Enter task ID: ")
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    tasks[task_id]["status"] = "complete"
    save_tasks()
    print(f"Task {task_id} marked as complete!")

def delete_task():
    """Delete a task."""
    print("\n=== Delete Task ===")
    
    task_id = input("Enter task ID: ")
    
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    # Bug: Missing confirmation before deletion
    confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ")
    if confirm.lower() != 'y':
        print("Task deletion cancelled.")
        return
    else:
        del tasks[task_id]
        save_tasks()
        print(f"Task {task_id} deleted successfully!")

def display_menu():
    """Display the main menu."""
    print("\n=== Task Tracker ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task")
    print("4. Update Task")
    # Bug: Missing option for marking task as complete
    print("5. Mark Task Complete")
    print("6. Delete Task")
    print("7. Exit")

def main():
    """Main application function."""
    load_tasks()
    
    while True:
        display_menu()
        
        # Bug: No validation on choice input
        choice = input("Enter your choice (1-7): ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 7:
            print("Invalid choice. Please enter a number between 1 and 7.")
            continue
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_task()
        elif choice == "4":
            update_task()
        elif choice == "5":
            mark_task_complete()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting Task Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 