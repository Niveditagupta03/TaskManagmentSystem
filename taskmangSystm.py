from tkinter import *
import json

tasks = []

def load_tasks_from_file():
    try:
        with open('tasks.txt', 'r') as file:
            content = file.read()
            if content:
                tasks_data = json.loads(content)
                for task_data in tasks_data:
                    tasks.append(task_data)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pass


def save_tasks_to_file():
    with open('tasks.txt', 'w') as file:
        json.dump(tasks, file)

def add_task():
    task_name = task_name_entry.get()
    task_description = task_description_entry.get()

    task = {
        'name': task_name,
        'description': task_description,
        'status': 'Incomplete'
    }
    tasks.append(task)
    update_task_list()
    save_tasks_to_file()
    clear_input_fields()

def view_tasks():
    task_list.delete(0, END)
    if len(tasks) == 0:
        task_list.insert(END, "No tasks found.")
    else:
        for task in tasks:
            task_list.insert(END, f"Name: {task['name']}")
            task_list.insert(END, f"Description: {task['description']}")
            task_list.insert(END, f"Status: {task['status']}")
            task_list.insert(END, "")

def mark_task_complete():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        if 0 <= task_index < len(tasks):
            tasks[task_index]['status'] = 'Complete'
            update_task_list()
            save_tasks_to_file()

def delete_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            update_task_list()
            save_tasks_to_file()

def create_task_list():
    task_list = Listbox(window, width=80, height=30)
    task_list.grid(row=4, column=0, columnspan=3, rowspan=8, pady=20)
    return task_list


def clear_input_fields():
    task_name_entry.delete(0, END)
    task_description_entry.delete(0, END)

def update_task_list():
    view_tasks()

# Load tasks from file (if exists)
load_tasks_from_file()

# Create the main window
window = Tk()
window.title("Task Management System")

# Create input fields and labels
task_name_label = Label(window, text="Task Name:")
task_name_label.grid(row=0, column=0)
task_name_entry = Entry(window)
task_name_entry.grid(row=0, column=1)

task_description_label = Label(window, text="Task Description:")
task_description_label.grid(row=1, column=0)
task_description_entry = Entry(window)
task_description_entry.grid(row=1, column=1)

# Create buttons
add_button = Button(window, text="Add Task", command=add_task)
add_button.grid(row=3, column=0, pady=20)

mark_complete_button = Button(window, text="Mark Task as Complete", command=mark_task_complete)
mark_complete_button.grid(row=3, column=1, pady=10)

delete_button = Button(window, text="Delete Task", command=delete_task)
delete_button.grid(row=3, column=2, pady=10)

# Create the task list
task_list_label = Label(window, text="Task List:")
task_list_label.grid(row=4, column=0, columnspan=3)
task_list = create_task_list()

# Update the task list
update_task_list()

window.mainloop()
