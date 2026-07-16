# Task Manager

A simple, personal to-do list app built with Django. Each user creates an
account and manages their own private list of tasks — nobody else can see
or edit them.

## Features

- **Accounts** — sign up, log in, log out
- **Create tasks** — title, description, priority (Low/Medium/High), optional due date
- **View tasks** — see all your tasks in one list
- **Edit tasks** — update any field, or mark a task as completed
- **Delete tasks** — remove tasks you no longer need
- **Filter** — view All / Pending / Completed tasks
- **Admin panel** — a superuser can view and manage all data directly

## Getting started

### 1. Install and run

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open your browser to **http://127.0.0.1:8000/**.

### 2. Create an account

- Click **Sign up** in the top navigation bar.
- Enter a username, email, and password, then submit.
- You're automatically logged in and taken to your (empty) task list.

Already have an account? Click **Login** instead.

## Using the app

### Viewing your tasks

After logging in, you land on the **My Tasks** page. This shows every task
you've created, sorted with incomplete, higher-priority, and soonest-due
tasks near the top.

Use the filter links at the top of the list to narrow the view:

| Filter | Shows |
|---|---|
| **All** | Every task you own |
| **Pending** | Tasks not yet marked complete |
| **Completed** | Tasks you've finished |

### Creating a task

1. Click **+ New Task** in the navigation bar.
2. Fill in:
   - **Title** — required, short summary of the task
   - **Description** — optional, more detail
   - **Priority** — Low, Medium, or High
   - **Due date** — optional
   - **Completed** — leave unchecked for a new task
3. Click **Save**. You're returned to your task list with the new task visible.

### Viewing task details

Click any task's title from the list to see its full details — description,
priority, due date, status, and when it was created.

### Editing a task

From the task list or the task detail page, click **Edit**. Update any
field and click **Save**. This is also how you mark a task as done: open
it, check the **Completed** box, and save.

### Deleting a task

Click **Delete** next to a task (from the list or detail page), then
confirm on the prompt that appears. This cannot be undone.

### Logging out

Click **Logout** in the top navigation bar. You'll need to log back in to
access your tasks again.

## Notes on privacy

Tasks are private to the account that created them — you can only view,
edit, or delete your own tasks, even if you know another task's URL.

## Admin access (optional)

If you created a superuser account (`python manage.py createsuperuser`),
you can log in at **http://127.0.0.1:8000/admin/** to browse and edit all
tasks and users across the whole app — useful for debugging or bulk
cleanup, not needed for normal day-to-day use.