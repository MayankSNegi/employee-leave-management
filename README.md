# Employee Leave Management System

## Overview

Employee Leave Management System is a full-stack web application that lets
employees register, log in, apply for leave, and track the status of their
requests, while administrators review employee records and approve or
reject leave applications. It is built with Python, Flask, and MySQL, and
uses server-rendered HTML with custom CSS and vanilla JavaScript — no
frontend framework required.

## Features

**Employee**
- Register and log in with a hashed password
- Personal dashboard with leave statistics (total / pending / approved / rejected)
- Apply for leave (Casual, Sick, Earned, Emergency, Unpaid) with date and reason validation
- View leave history with status badges and admin comments
- Cancel a leave request while it is still Pending
- Update profile (name, department)

**Administrator**
- Separate admin login and dashboard with company-wide statistics
- View every leave request with employee name, department, and dates
- Approve or reject requests with an optional (approve) or required (reject) comment
- Filter leave requests by status and department
- View all registered employees and their leave counts

**Security**
- Passwords hashed with Werkzeug (`generate_password_hash` / `check_password_hash`)
- Flask session-based authentication
- Role-based route protection (`@login_required`, `@employee_required`, `@admin_required`)
- Parameterized SQL queries (no string concatenation, no SQL injection)
- Server-side enforcement of business rules (e.g. only Pending leave can be cancelled)

## Technology Stack

- Python 3
- Flask
- MySQL
- HTML5
- CSS3 (custom, no framework)
- Vanilla JavaScript

## Project Structure

```
employee-leave-management/
│
├── app.py                 # Main Flask application (routes, business logic)
├── config.py               # Loads DB/secret configuration from environment
├── create_admin.py         # Interactive script to create an administrator
├── requirements.txt        # Python dependencies
├── .env.example             # Template for environment variables
├── .gitignore
│
├── database/
│   └── schema.sql          # Creates the database and all tables
│
├── templates/               # Jinja2 templates
│   ├── base.html            # Shared layout (sidebar, topbar, flash messages)
│   ├── login.html
│   ├── register.html
│   ├── employee_dashboard.html
│   ├── apply_leave.html
│   ├── my_leaves.html
│   ├── profile.html
│   ├── admin_dashboard.html
│   ├── admin_leaves.html
│   ├── admin_employees.html
│   ├── 403.html
│   ├── 404.html
│   └── 500.html
│
└── static/
    ├── css/style.css        # All styling
    └── js/script.js         # Flash auto-hide, mobile nav, confirmations, validation
```

## Prerequisites

- Python 3.9+
- MySQL Server (locally installed and running)
- pip
- VS Code (recommended)
- Git (optional, for version control)

## Installation

```bash
git clone <repository-url>
cd employee-leave-management

python -m venv venv
```

Activate the virtual environment:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## MySQL Setup

1. Start your MySQL server.
2. Run the schema file to create the database and tables.

**Using the MySQL command line:**

```bash
mysql -u root -p
```

Then inside the MySQL prompt:

```sql
SOURCE database/schema.sql;
```

**Using MySQL Workbench:**

Open MySQL Workbench → connect to your local server → open
`database/schema.sql` → click the execute (lightning bolt) button.

This creates the `employee_leave_management` database along with the
`users` and `leave_requests` tables.

## Environment Setup

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and set your own values:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DB=employee_leave_management
SECRET_KEY=YOUR_SECRET_KEY
```

To generate a strong `SECRET_KEY`, you can run:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output as the value of `SECRET_KEY`.

## Create Administrator

With your virtual environment activated and `.env` configured, run:

```bash
python create_admin.py
```

You will be prompted for an Admin ID, full name, email, and password. The
password is hashed before it is stored, and the script prevents creating a
duplicate admin with the same email or Admin ID.

## Run Application

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

## Employee Workflow

1. Go to `/register` and create an employee account (department and
   Employee ID are required; role is always set to `employee`).
2. Log in at `/login`.
3. From the Employee Dashboard, click **Apply Leave** and submit a request.
4. Track its status on **My Leave Requests** — pending requests can be
   cancelled; approved/rejected ones cannot.
5. Update your name/department from **Profile**.

## Admin Workflow

1. Create an administrator with `python create_admin.py` (see above).
2. Log in at `/login` using the admin's email and password.
3. From the Admin Dashboard, view company-wide statistics.
4. Go to **Leave Requests** to review, filter by status/department, and
   Approve or Reject each request (rejecting requires a comment).
5. Go to **Employees** to see all registered employees and their leave counts.

## Windows / VS Code Quick Start

```bash
# 1. Open the project folder in VS Code, then open a terminal

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment template and edit it
copy .env.example .env

# 5. Set up MySQL (via MySQL Workbench or CLI)
mysql -u root -p
SOURCE database/schema.sql;

# 6. Create the administrator account
python create_admin.py

# 7. Run the app
python app.py

# 8. Open in browser
http://127.0.0.1:5000
```

## Troubleshooting

**MySQL connection refused**
Make sure the MySQL service is running (`services.msc` on Windows, or
`sudo service mysql start` / `brew services start mysql` on
Linux/macOS), and that `MYSQL_HOST` and `MYSQL_PORT` in `.env` are correct.

**Access denied for MySQL user**
Double-check `MYSQL_USER` and `MYSQL_PASSWORD` in `.env` match a valid
MySQL account. You can verify credentials with:
`mysql -u <user> -p`

**Unknown database 'employee_leave_management'**
The schema hasn't been applied yet. Run `database/schema.sql` as described
in the MySQL Setup section — it creates the database automatically.

**ModuleNotFoundError**
Your virtual environment is either not activated or dependencies aren't
installed. Activate `venv` and run `pip install -r requirements.txt` again.

**Port already in use**
Another process is using port 5000. Stop it, or run the app on a different
port: `flask run --port 5001` (or edit `app.run(debug=True, port=5001)` in
`app.py`).

**Incorrect .env configuration**
Confirm `.env` exists in the project root (copied from `.env.example`) and
that there are no extra spaces or quotes around the values.

**Virtual environment not activated**
Your terminal prompt should show `(venv)` at the start of the line. If not,
re-run the activation command for your OS shown above.
