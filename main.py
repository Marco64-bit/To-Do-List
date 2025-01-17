import json
from datetime import date
import calendar

TO_DO = {}
users = []
options = [1, 2, 3, 4, 5, 6, 7]
priorities = ('high', 'medium', 'low')
status = ('pending', 'done')
properties = ('priority', 'status', 'due_date')
ur_options = ["1", "2"]

USER_FILE_PATH = r"all_users.json"

def load_users():
    global users
    file = open(USER_FILE_PATH, "r")
    content = file.read()
    file.close()
    
    if content.strip() == "":
        print(f"The user file is empty. Initializing with an empty list.")
        users = []
    else:
        users = json.loads(content)

def save_users():
    global users
    file = open(USER_FILE_PATH, "w")
    json.dump(users, file, indent=4)
    file.close()

def load_tasks(username):
    file_path = f"users_tasks\\tasks_{username}.json"
    try:
        file = open(file_path, "r")
        content = file.read()
        file.close()
        
        if content.strip() == "":
            print(f"No tasks found for user '{username}'. A new task list will be created.")
            return {}
        else:
            return json.loads(content)
    except FileNotFoundError:
        print(f"You are new User '{username}'. A new task list will be created.")
        return {}

def save_tasks(username):
    global TO_DO
    file_path = f"users_tasks\\tasks_{username}.json"
    file = open(file_path, "w")
    json.dump(TO_DO, file, indent=4)
    file.close()
    print("All Tasks Saved!")

def ur_name_check(user_name):
    while not user_name.isalnum():
        user_name = input("Invalid username. Enter a valid username: ").strip()
    return user_name

def email_check(email):
    while "@" not in email or "." not in email:
        email = input("Invalid email. Enter a valid email: ").strip()
    return email

def pass_check(password):
    while len(password) < 8:
        password = input("Password must be at least 8 characters long. Enter your password again: ").strip()
    return password

def user_exists(email, username):
    for user in users:
        if user.get("email") == email:
            return "email"
        if user.get("username") == username:
            return "username"
    return None

def user_authentication():
    global TO_DO
    print("========================Hello!========================")
    print("1- Sign_up\n2- Login")
    selection = input("Enter your choice: ").strip()
    selection = selection_check(selection)

    if int(selection) == 1:
        while True:
            user_name = input("Enter your username(q to Quti): ").strip()
            if user_name.lower() == "q":
                return user_authentication()
            user_name = ur_name_check(user_name)
            email = input("Enter your email: ").strip()
            email = email_check(email)
            existing = user_exists(email, user_name)
            if existing == "email":
                print("This email is already registered. Please use a different email.")
                continue
            elif existing == "username":
                print("This username is already taken. Please choose a different username.")
                continue

            password = input("Enter your password: ").strip()
            password = pass_check(password)

            registration = {"username": user_name, "email": email, "password": password}
            users.append(registration)
            save_users()

            print(f"User  '{user_name}' registered successfully!")
            print("Please log in to continue.")
            return user_authentication()  

    elif int(selection) == 2:
        while True:
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()

            for user in users:
                if user["email"] == email:
                    if user["password"] == password:
                        print(f"Login successful! Welcome, {user['username']}")
                        TO_DO.update(load_tasks(user['username']))
                        return user['username']
                    else:
                        print("Incorrect password. Please try again.")
                        break

            print("No account found with this email. Please sign up first.")
            return user_authentication() 

def selection_check(selection):
    while selection not in ur_options:
        print("Invalid option, select between (1 or 2)")
        selection = input("Enter your choice: ").strip()
    return selection

def add_function(option):
    global TO_DO
    if int(option) == 1:
        num_task = input("Enter number of tasks you want to add(q to Quit): ")
        if num_task.lower() == "q":
            start_menu()
        while not num_task.isdigit():
            print("Invalid input!")
            num_task = input("Enter number of tasks you want to add(q to Quit): ")
            if num_task.lower() == "q":
                start_menu()
        for i in range(int(num_task)):
            task_name = input("Enter the Task Name(q to Quit): ").lower()
            if task_name.lower() == "q":
                start_menu()
            while task_name.strip() == "":
                print("Task name is required!")
                task_name = input("Enter the Task Name(q to Quit): ").lower()
                if task_name.lower() == "q":
                    start_menu()
            while True:
                priority = input("Enter the Task priority (High, Medium, Low): ").lower().strip()
                if priority.lower() == "q":
                    start_menu()
                if priority not in priorities:
                    print("Invalid Priority")
                else:
                    break
            Due_Date = due_date(task_name)
            task = {
                "priority": priority,
                "Due-Date": Due_Date,
                "status": "pending"
            }
            TO_DO[task_name] = task

def save_function(username):
    global TO_DO
    save_tasks(username)

def due_date(task_name):
    global TO_DO
    global current_date
    global year

    current_date = date.today()
    year = input(f"Enter the year ({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
    if year.strip() == "cancel":
        start_menu()
    else:
        year = require_year(year)
    month = check_month_in_year()
    month = require_month(month)
    total_days = calendar.monthrange(int(year), int(month))[1]
    day = require_day(total_days)
    due_date = str(date(int(year), int(month), int(day)))

    return due_date

def remove_function():
    global TO_DO
    while True:
        re_task = input("Enter the Task Name you want to remove(q to quit): ").lower().strip()
        task_found = False
        if re_task.lower() == "q":
            break
        for task in TO_DO:
            if re_task == task:
                TO_DO.pop(task)
                print(f"Task '{re_task}' removed successfully.")
                task_found = True
                break
        if task_found:
            break
        else:
            print("Task not found. Please try again.")

def edit_task():
    global TO_DO
    global data
    data = TO_DO

    while True:
        print("========================Tasks========================")
        for key in data:
            print(key)
        task_name = input("Enter the task name you want to edit (Q to quit): ").strip().lower()
        if task_name == "q":
            start_menu()
        while task_name not in data:
            print("Task not found")
            task_name = input("Enter the task name you want to edit(q to quit): ").strip()
            if task_name == "q":
                start_menu()
        specify_field = input("Choose between (priority, status, due_date) to edit or cancel: ").lower().strip()
        while specify_field not in properties and specify_field != 'cancel':
            print("Task Field not found")
            specify_field = input("Choose between (priority, status, due_date) to edit or cancel: ").lower().strip()
        else:
            if specify_field == 'priority':
                edit_priority(specify_field, task_name)
            elif specify_field == 'status':
                edit_status(specify_field, task_name)
            elif specify_field == 'due_date':
                edit_due_date(specify_field, task_name)
            elif specify_field == 'cancel':
                edit_task()

def edit_priority(specify_field, task_name):
    global data
    update_priority = input("Change the priority to (high, medium, low) or cancel: ").lower().strip()
    while update_priority not in priorities and update_priority != 'cancel':
        print("Invalid priority input")
        update_priority = input("Change the priority to (high, medium, low) or cancel: ").lower().strip()
    else:
        if update_priority == 'cancel':
            edit_task()
        elif update_priority in priorities:
            data[task_name][specify_field] = update_priority
            print(f"The priority in {task_name} changed to '{update_priority}' successfully")

def edit_status(specify_field, task_name):
    global data
    update_status = input("Change the status to (pending, done) or cancel: ").lower().strip()
    while update_status not in status and update_status != 'cancel':
        print("Invalid status input")
        update_status = input("Change the status to (pending, done) or cancel: ").lower().strip()
    else:
        if update_status == 'cancel':
            edit_task()
        elif update_status in status:
            data[task_name][specify_field] = update_status
            print(f"The status in {task_name} changed to '{update_status}' successfully!")

def edit_due_date(specify_field, task_name):
    global data
    global current_date
    global year

    current_date = date.today()
    year = input(f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
    if year.strip() == "cancel":
        edit_task()
    else:
        year = require_year(year)
    month = check_month_in_year()
    month = require_month(month)
    total_days = calendar.monthrange(int(year), int(month))[1]
    day = require_day(total_days)
    update_due_date = date(int(year), int(month), int(day))
    data[task_name]["Due-Date"] = str(update_due_date)
    print(f"The due date in {task_name} changed to '{update_due_date}' successfully!")

def require_year(year):
    global data
    while year.strip() == "":
        print("Year is required!")
        year = input(f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
    if not year.isdigit() and year.strip() != "cancel":
        year = is_year_not_digit(year)
    elif not (current_date.year <= int(year) <= current_date.year + 4) and year.strip() != "cancel":
        year = check_year_range(year)
    elif year.strip() == "cancel":
        edit_task()
    return year

def is_year_not_digit(year):
    global data
    if year.strip() == "":
        year = require_year(year)
    while not year.isdigit() and year.strip() != "cancel":
        print("Year should be number only!")
        year = input(f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
        if year.strip() == "":
            year = require_year(year)
    else:
        if year.strip() == "cancel":
            edit_task()
        elif not (current_date.year <= int(year) <= current_date.year + 4):
            year = check_year_range(year)
    return year

def check_year_range(year):
    global data
    if year.strip() == "":
        year = require_year(year)
    elif not year.isdigit() and year.strip() != "cancel":
        edit_task()
    while not (current_date.year <= int(year) <= current_date.year + 4) and year.strip() != "cancel":
        print("Wrong Year Range")
        year = input(f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
        if year.strip() == "":
            year = require_year(year)
        elif year.strip() == "cancel":
            edit_task()
        elif not year.isdigit():
            year = is_year_not_digit(year)
    else:
        if year.strip() == "cancel":
            edit_task()
    return year

def check_month_in_year():
    global data
    global month
    if int(year) == current_date.year:
        if current_date.month == 12:
            month = input(f"Enter the month({current_date.month}) or cancel: ").strip().lower()
        else:
            month = input(f"Enter the month({current_date.month} - 12) or cancel: ").strip().lower()
    else:
        month = input(f"Enter the month(1 - 12) or cancel: ").strip().lower()
    return month

def require_month(month):
    global data
    while month.strip() == "":
        print("Month is required!")
        month = check_month_in_year()
    else:
        if month == "cancel":
            edit_task()
        elif not month.isdigit():
            month = is_month_not_digit(month)
        elif not (1 <= int(month) <= 12):
            month = check_month_range(month)
    if month.strip() == "cancel":
        edit_task()
    elif not month.isdigit():
        month = is_month_not_digit(month)
    if int(year) == current_date.year:
        if not (current_date.month <= int(month) <= 12):
            month = check_month_range(month)
    else:
        if not (1 <= int(month) <= 12):
            month = check_month_range(month)
    return month

def is_month_not_digit(month):
    global data
    if month.strip() == "":
        month = require_month(month)
    while not month.isdigit():
        print("Month should be number only!")
        month = check_month_in_year()
        if month.strip() == "":
            month = require_month(month)
    if int(year) == current_date.year:
        if not (current_date.month <= int(month) <= 12):
            month = check_month_range(month)
    else:
        if not (1 <= int(month) <= 12):
            month = check_month_range(month)
    return month

def check_month_range(month):
    global data
    if month.strip() == "":
        month = require_month(month)
    elif not month.isdigit():
        month = is_month_not_digit(month)

    if int(year) == current_date.year:
        while not (current_date.month <= int(month) <= 12):
            print("Wrong month Range")
            month = check_month_in_year()
            if month.strip() == "":
                month = require_month(month)
            if not month.isdigit():
                month = is_month_not_digit(month)
    else:
        while not (1 <= int(month) <= 12):
            print("Wrong month Range")
            month = input(f"Enter the month(1 - 12) or cancel: ").strip().lower()
            if month.strip() == "":
                month = require_month(month)
            elif month.strip() == "cancel":
                edit_task()
            elif not month.isdigit():
                month = is_month_not_digit(month)
    return month

def require_day(total_days):
    global data
    if int(year) == current_date.year and int(month) == current_date.month:
        day = input(f"Enter the day({current_date.day} - {total_days}) or cancel: ").strip().lower()
    else:
        day = input(f"Enter the day(1 - {total_days}) or cancel: ").strip().lower()
    while day.strip() == "":
        print("Day is required!")
        day = require_day(total_days)
    else:
        day = is_day_valid(day, total_days)
    if day.strip() == "cancel":
        edit_task()
    elif not day.isdigit():
        day = is_day_not_digit(day, total_days)
    if int(year) == current_date.year and int(month) == current_date.month:
        if not (current_date.day <= int(day) <= total_days):
            day = correct_day(day, total_days)
    else:
        if not (1 <= int(day) <= total_days):
            day = correct_day(day, total_days)
    return day

def is_day_valid(day, total_days):
    global data
    if not day.isdigit():
        day = is_day_not_digit(day, total_days)
    elif day.strip() == "cancel":
        edit_task()
    elif int(year) == current_date.year and int(month) == current_date.month:
        if not (current_date.day <= int(day) <= total_days) and day.strip():
            day = check_day_range(day, total_days)
    else:
        if not (1 <= int(day) <= total_days):
            day = check_day_range(day, total_days)
    return day

def is_day_not_digit(day, total_days):
    global data
    if day.strip() == "":
        day = require_day(total_days)
    while not day.isdigit() and day.strip() != "cancel":
        print("Day should be number only!")
        day = require_day(total_days)
        if day.strip() == "":
            day = require_day(total_days)
    else:
        if day.strip() == "cancel":
            edit_task()
        else:
            day = is_day_valid(day, total_days)
    return day

def correct_day(day, total_days):
    global data
    if int(year) == current_date.year and int(month) == current_date.month:
        while not (current_date.day <= int(day) <= total_days):
            print("Wrong Day Range")
            day = input(f"Enter the Day({current_date.day} - {total_days}) or cancel: ").strip().lower()
            if day.strip() == "":
                day = require_day(total_days)
            elif day.strip() == "cancel":
                edit_task()
            elif not day.isdigit():
                day = is_day_not_digit(day, total_days)
    else:
        while not (1 <= int(day) <= total_days):
            print("Wrong day Range")
            day = input(f"Enter the Day(1 - {total_days}) or cancel: ").strip().lower()
            if day.strip() == "":
                day = require_day(total_days)
            elif day.strip() == "cancel":
                edit_task()
            elif not day.isdigit():
                day = is_day_not_digit(day, total_days)
    return day

def check_day_range(day, total_days):
    global data
    if day.strip() == "":
        day = require_day(total_days)
    elif day.strip() == "cancel":
        edit_task()
    elif not day.isdigit():
        day = is_day_not_digit(day, total_days)
    if int(year) == current_date.year:
        day = correct_day(day, total_days)
    else:
        day = correct_day(day, total_days)
    return day

def sort_tasks():
    global TO_DO
    while True:
        sort_option = input(
            "Do you want to sort by priority or due date? (Enter 'priority' or 'due date'): ").strip().lower()
        if sort_option == 'priority':
            sorted_tasks = dict(sorted(TO_DO.items(), key=lambda item: priorities.index(item[1]['priority'])))
            TO_DO = sorted_tasks
            print("Tasks sorted by priority!")
            start_menu()
        elif sort_option == 'due date':
            sorted_tasks = dict(sorted(TO_DO.items(), key=lambda item: item[1]['Due-Date']))
            TO_DO = sorted_tasks
            print("Tasks sorted by due date!")
            start_menu()
        else:
            print("Invalid option. Please choose 'priority' or 'due date'.")

def search_function():
    global TO_DO
    while True:
        search_term = input("Enter the task name to search (or type 'cancel' to go back): ").lower().strip()
        if search_term == 'cancel':
            return
        if search_term == "":
            print("You must enter a task name to search. Please try again.")
            continue
        found = False
        print("========================Search Results========================")
        print("Tasks".ljust(30) + "Priority".ljust(15) + "Due-date".ljust(15) + "Status".ljust(10))

        for task, details in TO_DO.items():
            if search_term in task.lower():
                print(
                    f"{task.ljust(30)}{details['priority'].ljust(15)}{details['Due-Date'].ljust(15)}{details['status'].ljust(10)}")
                found = True
        if not found:
            print("No tasks found matching your search. Please try again.")
        else:
            break

def start_menu():
    global username
    while True:
        print()
        print("-" * 80)
        print(f"                    TO-DO-LIST!                                     ")
        print("-" * 80)
        print("Tasks".ljust(30) + "Priority".ljust(15) + "Due-date".ljust(15) + "Status".ljust(10))

        for task in TO_DO:
            print(
                f"{task.ljust(30)}{TO_DO[task]['priority'].ljust(15)}{TO_DO[task]['Due-Date'].ljust(15)}{TO_DO[task]['status'].ljust(10)}")
        print()
        print("-" * 50)
        print(f"                    OPTIONS                  ")
        print("-" * 50)
        print("1- ADD \n2- REMOVE \n3- EDIT \n4- SAVE \n5- SORT\n6- SEARCH\n7- Logout")
        option = input("Enter your option: ")
        if option == "7":
            print("Exiting the program. Goodbye!")
            exit()
        while not option.isdigit():
            print("Enter a number (1:7)!") 
            option = input("Enter your option: ")
        while True:
            if int(option) not in options:
                print("Invalid Option")
                option = input("Enter your option: ")
            else:
                break
        if option == "1":
            add_function(option)
        elif option == "2":
            remove_function()
        elif option == "3":
            edit_task()
        elif option == "4":
            save_function(username)
        elif option == "5":
            sort_tasks()
        elif option == "6":
            search_function()

if __name__ == "__main__":
    load_users()
    username = user_authentication()
    if username:
        start_menu()