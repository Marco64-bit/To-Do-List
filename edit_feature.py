from datetime import date
import json
import calendar


def edit_task():
    global data
    file = open("all_tasks.json", 'r')
    data = json.load(file)
    while True:
        print("========================Tasks========================")
        for key in data:
            print(key)
        task_name = input("Enter the task name you want to edit: ").strip()
        while task_name not in data:
            print("Task not found")
            task_name = input("Enter the task name you want to edit: ").strip()

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
    update_priority = input(
        "Change the priority to (high, medium, low) or cancel: ").lower().strip()
    while update_priority not in priorities and update_priority != 'cancel':
        print("Invalid priority input")
        update_priority = input(
            "Change the priority to (high, medium, low) or cancel: ").lower().strip()
    else:
        if update_priority == 'cancel':
            edit_task()
        elif update_priority in priorities:
            data[task_name][specify_field] = update_priority
            file = open('all_tasks.json', 'w')
            json.dump(data, file, indent=4)
            file.close()
            print(f"The priority in {task_name} changed to '{update_priority}' successfully")


def edit_status(specify_field, task_name):
    update_status = input("Change the status to (pending, done) or cancel: ").lower().strip()
    while update_status not in status and update_status != 'cancel':
        print("Invalid status input")
        update_status = input("Change the status to (pending, done) or cancel: ").lower().strip()
    else:
        if update_status == 'cancel':
            edit_task()
        elif update_status in status:
            data[task_name][specify_field] = update_status
            file = open('all_tasks.json', 'w')
            json.dump(data, file, indent=4)
            file.close()
            print(f"The status in {task_name} changed to '{update_status}' successfully!")


def edit_due_date(specify_field, task_name):
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
    data[task_name][specify_field] = str(update_due_date)
    file = open('all_tasks.json', 'w')
    json.dump(data, file, indent=4)
    file.close()
    print(f"The status in {task_name} changed to '{update_due_date}' successfully!")


def require_year(year):
    while year.strip() == "":
        print("Year is required!")
        year = input(
            f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
    if not year.isdigit() and year.strip() != "cancel":
        year = is_year_not_digit(year)
    elif not (current_date.year <= int(year) <= current_date.year + 4) and year.strip() != "cancel":
        year = check_year_range(year)
    elif year.strip() == "cancel":
        edit_task()
    return year


def is_year_not_digit(year):
    if year.strip() == "":
        year = require_year(year)
    while not year.isdigit() and year.strip() != "cancel":
        print("Year should be number only!")
        year = input(
            f"Enter the year({current_date.year} - {current_date.year + 4}) or cancel: ").strip().lower()
        if year.strip() == "":
            year = require_year(year)
    else:
        if year.strip() == "cancel":
            edit_task()
        elif not (current_date.year <= int(year) <= current_date.year + 4):
            year = check_year_range(year)
    return year


def check_year_range(year):
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


def is_day_valid(day, total_days):
    if not day.isdigit():
        day = is_day_not_digit(day, total_days)
    elif day.strip() == "cancel":
        edit_task()
    elif int(year) == current_date.year and int(month)==current_date.month:
        if not(current_date.day <= int(day) <= total_days) and day.strip():
            day = check_day_range(day, total_days)
    else:
        if not(1<=int(day)<=total_days):
            day = check_day_range(day, total_days)
    return day


def require_day(total_days):
    if int(year) == current_date.year and int(month)==current_date.month:
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
    if int(year) == current_date.year and int(month)==current_date.month:
        if not(current_date.day <= int(day) <= total_days):
            day = check_day_range(day, total_days)
    else:
        if not(1<=int(day)<=total_days):
            day = check_day_range(day, total_days)
    return day


def is_day_not_digit(day, total_days):
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
    if int(year) == current_date.year and int(month)==current_date.month:
        while not(current_date.day <= int(day) <= total_days):
            print("Wrong Day Range")
            day = input(f"Enter the Day({current_date.day} - {total_days}) or cancel: ").strip().lower()
            if day.strip() == "":
                day = require_day(total_days)
            elif day.strip() == "cancel":
                edit_task()
            elif not day.isdigit():
                day = is_day_not_digit(day, total_days)
    else:
        while not(1<=int(day)<=total_days):
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

priorities = ('high', 'medium', 'low')
status = ('pending', 'done')
properties = ('priority', 'status', 'due_date')

edit_task()

