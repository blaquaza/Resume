import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def load_users():
    """
    Load user data from user.txt into a dictionary.
    """
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        if user:
            username, password = user.split(";")
            username_password[username] = password

    return username_password


def load_tasks():
    """
    Load tasks from tasks.txt into a list of dictionaries.
    """
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t["username"] = task_components[0]
        curr_t["title"] = task_components[1]
        curr_t["description"] = task_components[2]
        curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t["completed"] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list


def save_users(username_password):
    """
    Save the user data back to user.txt.
    """
    with open("user.txt", "w") as user_file:
        user_data = [f"{username};{password}" for username, password in username_password.items()]
        user_file.write("\n".join(user_data))


def save_tasks(task_list):
    """
    Save the task list back to tasks.txt.
    """
    with open("tasks.txt", "w") as task_file:
        task_data = []
        for task in task_list:
            task_str = ";".join([
                task["username"],
                task["title"],
                task["description"],
                task["due_date"].strftime(DATETIME_STRING_FORMAT),
                task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task["completed"] else "No"
            ])
            task_data.append(task_str)
        task_file.write("\n".join(task_data))


def reg_user(username_password):
    """
    Register a new user, ensuring no duplicate usernames.
    """
    while True:
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Error: Username already exists. Please choose a different username.")
        else:
            break

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        username_password[new_username] = new_password
        save_users(username_password)
        print("New user registered successfully.")
    else:
        print("Error: Passwords do not match.")


def add_task(task_list, username_password):
    """
    Add a new task and save it to tasks.txt.
    """
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("Error: User does not exist. Please enter a valid username.")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")

    curr_date = date.today()

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")


def view_all(task_list):
    """
    Display all tasks in a user-friendly format.
    """
    for i, task in enumerate(task_list, 1):
        print(f"Task {i}:")
        print(f"  Title: {task['title']}")
        print(f"  Assigned to: {task['username']}")
        print(f"  Assigned date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"  Due date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"  Completed: {'Yes' if task['completed'] else 'No'}")
        print(f"  Description: {task['description']}")
        print("-" * 40)


def view_mine(task_list, curr_user):
    """
    Display tasks assigned to the current user and allow interaction.
    """
    user_tasks = [task for task in task_list if task["username"] == curr_user]

    if not user_tasks:
        print("You have no tasks assigned.")
        return

    for i, task in enumerate(user_tasks, 1):
        print(f"Task {i}:")
        print(f"  Title: {task['title']}")
        print(f"  Due date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"  Completed: {'Yes' if task['completed'] else 'No'}")
        print(f"  Description: {task['description']}")
        print("-" * 40)

    while True:
        try:
            task_choice = int(input("Select a task number to modify or enter -1 to return to the main menu: "))
            if task_choice == -1:
                return
            elif 1 <= task_choice <= len(user_tasks):
                chosen_task = user_tasks[task_choice - 1]
                if chosen_task["completed"]:
                    print("Error: You cannot edit a completed task.")
                else:
                    modify_task(chosen_task)
                save_tasks(task_list)
                return
            else:
                print("Error: Invalid task number.")
        except ValueError:
            print("Error: Please enter a valid number.")


def modify_task(task):
    """
    Allow the user to modify a task's due date or assigned user.
    """
    while True:
        print("1. Mark task as complete")
        print("2. Edit task")
        choice = input("Enter your choice: ")

        if choice == "1":
            task["completed"] = True
            print("Task marked as complete.")
            break
        elif choice == "2":
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
            try:
                task["due_date"] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                print("Due date updated.")
                break
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
        else:
            print("Error: Invalid choice. Please try again.")
        
def generate_reports(task_list, username_password):
    
    '''Generate task_overview.txt and user_overview.txt reports.'''
    
    #Task overview
    total_tasks = len(task_list)
    completed_tasks = len([task for task in task_list if task["completed"]])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = len([task for task in task_list if not task["completed"] and task["due_date"] < datetime.now()])
    incomplete_percentage = (uncompleted_tasks / total_tasks * 100) if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview Report\n")
        task_overview_file.write("---------------------\n")
        task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
        task_overview_file.write(f"Number of completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Number of uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Number of overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # User overview
    total_users = len(username_password)
    user_reports = []

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview Report\n")
        user_overview_file.write("---------------------\n")
        user_overview_file.write(f"Total number of users: {total_users}\n")
        user_overview_file.write(f"Total number of tasks: {total_tasks}\n")

        for user, password in username_password.items():
            user_tasks = [task for task in task_list if task["username"] == user]
            num_user_tasks = len(user_tasks)
            user_task_percentage = (num_user_tasks / total_tasks * 100) if total_tasks > 0 else 0
            completed_tasks = len([task for task in user_tasks if task["completed"]])
            uncompleted_tasks = num_user_tasks - completed_tasks
            overdue_tasks = len([task for task in user_tasks if not task["completed"] and task["due_date"] < datetime.now()])
            completed_percentage = (completed_tasks / num_user_tasks * 100) if num_user_tasks > 0 else 0
            uncompleted_percentage = (uncompleted_tasks / num_user_tasks * 100) if num_user_tasks > 0 else 0
            overdue_percentage = (overdue_tasks / num_user_tasks * 100) if num_user_tasks > 0 else 0

            user_reports.append(f"User: {user}\n"
                                f"Total tasks assigned: {num_user_tasks}\n"
                                f"Percentage of total tasks: {user_task_percentage:.2f}%\n"
                                f"Percentage completed: {completed_percentage:.2f}%\n"
                                f"Percentage incomplete: {uncompleted_percentage:.2f}%\n"
                                f"Percentage overdue: {overdue_percentage:.2f}%\n")

        user_overview_file.write("\n".join(user_reports))


def display_statistics():
    """
    Display statistics for tasks and users from reports. Generate reports if they do not exist.
    """
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Reports do not exist. Generating reports...")
        generate_reports(task_list, username_password)

    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())

    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())


# ===== Main Menu =====
username_password = load_users()
task_list = load_tasks()

logged_in = False

# Login section
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user not in username_password:
        print("Error: User does not exist.")
    elif username_password[curr_user] != curr_pass:
        print("Error: Incorrect password.")
    else:
        print("Login successful!")
        logged_in = True

# Main menu loop
while True:
    print()
    menu = input('''Select one of the following options:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r' and curr_user == 'admin':
        reg_user(username_password)
    elif menu == 'a':
        add_task(task_list, username_password)
    elif menu == 'va':
        view_all(task_list)
    elif menu == 'vm':
        view_mine(task_list, curr_user)
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports(task_list, username_password)
        print("Reports generated successfully.")
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
    elif menu == 'e':
        print("Goodbye!")
        break
    else:
        print("Error: Invalid choice or insufficient permissions.")
