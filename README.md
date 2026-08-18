# Employee Leave Management System

A full-stack **Employee Leave Management System** built with **Python, Flask, MySQL, Jinja2, HTML5, CSS3, and Vanilla JavaScript**.

The system provides separate workflows for **employees** and **administrators**. Employees can create accounts, submit leave requests, track request status, cancel pending requests, and manage their profiles. Administrators can manage leave applications, approve or reject requests, filter requests, and view employee records and leave statistics.

---

## 📌 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [User Roles](#-user-roles)
* [Application Workflow](#-application-workflow)
* [Technology Stack](#-technology-stack)
* [Project Architecture](#-project-architecture)
* [Project Structure](#-project-structure)
* [Database Design](#-database-design)
* [Security](#-security)
* [Validation and Business Rules](#-validation-and-business-rules)
* [Prerequisites](#-prerequisites)
* [Installation and Setup](#-installation-and-setup)
* [MySQL Database Setup](#-mysql-database-setup)
* [Environment Configuration](#-environment-configuration)
* [Creating an Administrator](#-creating-an-administrator)
* [Running the Application](#-running-the-application)
* [Employee Guide](#-employee-guide)
* [Administrator Guide](#-administrator-guide)
* [Application Routes](#-application-routes)
* [Database Schema](#-database-schema)
* [Error Handling](#-error-handling)
* [Troubleshooting](#-troubleshooting)
* [Future Enhancements](#-future-enhancements)
* [Learning Outcomes](#-learning-outcomes)
* [Contributing](#-contributing)
* [License](#-license)
* [Author](#-author)

---

## 📖 Overview

The **Employee Leave Management System** is a web-based application designed to simplify and digitize the employee leave management process.

Traditional leave management can involve manual forms, emails, spreadsheets, and difficult-to-track approval processes. This application provides a centralized platform where employees can submit and monitor leave requests while administrators can efficiently review and manage them.

The application follows a role-based architecture:

```text
                         Employee Leave Management System
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                Employee                            Administrator
                    │                                   │
          ┌─────────┼─────────┐              ┌──────────┼──────────┐
          │         │         │              │          │          │
       Register   Apply    Track Leave    Dashboard  Review     Employees
       / Login    Leave    Requests       Statistics Requests    List
          │         │         │                         │
          └─────────┴─────────┘                         │
                                                        │
                                             Approve / Reject
```

---

## ✨ Features

### 👨‍💼 Employee Features

* Employee registration
* Secure employee login
* Password hashing using Werkzeug
* Employee dashboard
* Leave statistics:

  * Total requests
  * Pending requests
  * Approved requests
  * Rejected requests
* Apply for leave
* Supported leave types:

  * Casual Leave
  * Sick Leave
  * Earned Leave
  * Emergency Leave
  * Unpaid Leave
* Start and end date selection
* Automatic leave-day calculation
* Leave reason submission
* Leave history
* Leave status tracking
* Admin comments visibility
* Cancel pending leave requests
* Profile management
* Update name and department
* Session-based authentication

---

### 🛡️ Administrator Features

* Separate administrator account creation
* Secure administrator login
* Administrator dashboard
* Company-wide leave statistics
* View all leave requests
* View employee name and department
* View leave dates and duration
* Approve leave requests
* Reject leave requests
* Optional comments when approving
* Required comments when rejecting
* Filter requests by:

  * Status
  * Department
* View all registered employees
* View employee leave counts
* Role-based access control

---

## 👥 User Roles

The application supports two roles.

| Role              | Description                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| **Employee**      | Registers, logs in, applies for leave, tracks requests, cancels pending requests, and manages profile |
| **Administrator** | Reviews leave requests, approves/rejects requests, filters applications, and manages employee records |

### Employee

Employees are created through the registration page.

The employee role is automatically assigned during registration and cannot be selected by the user.

### Administrator

Administrators are created separately using:

```bash
python create_admin.py
```

This prevents normal users from registering themselves as administrators.

---

## 🔄 Application Workflow

### Employee Workflow

```text
Register
   ↓
Login
   ↓
Employee Dashboard
   ↓
Apply for Leave
   ↓
Leave Request Created
   ↓
Pending
   ↓
Administrator Reviews Request
   ↓
┌───────────────┴───────────────┐
↓                               ↓
Approved                     Rejected
↓                               ↓
Employee Notified             Comment Visible
```

### Administrator Workflow

```text
Create Admin Account
        ↓
      Login
        ↓
Admin Dashboard
        ↓
View Leave Requests
        ↓
Filter by Status / Department
        ↓
Review Application
        ↓
┌───────────────┴───────────────┐
↓                               ↓
Approve                        Reject
↓                               ↓
Optional Comment             Required Comment
```

---

# 🛠️ Technology Stack

## Backend

* **Python 3**
* **Flask 3.0.3**
* **MySQL Connector/Python 8.4.0**
* **python-dotenv 1.0.1**
* **Werkzeug Security**

## Frontend

* **HTML5**
* **CSS3**
* **Jinja2 Templates**
* **Vanilla JavaScript**

## Database

* **MySQL**
* InnoDB storage engine
* Foreign key relationships
* Indexed leave request fields
* `utf8mb4` character set

## Development Tools

* Visual Studio Code
* MySQL Workbench
* Git
* GitHub
* Python Virtual Environment

---

# 🏗️ Project Architecture

The application follows a simple server-rendered web architecture.

```text
┌─────────────────────────────────────┐
│              Browser                │
│      HTML + CSS + JavaScript        │
└──────────────────┬──────────────────┘
                   │
                   │ HTTP Requests
                   ▼
┌─────────────────────────────────────┐
│              Flask                  │
│                                     │
│  Routes                             │
│  Authentication                     │
│  Authorization                      │
│  Validation                         │
│  Business Logic                     │
│  Session Management                 │
└──────────────────┬──────────────────┘
                   │
                   │ SQL Queries
                   ▼
┌─────────────────────────────────────┐
│              MySQL                  │
│                                     │
│  users                              │
│  leave_requests                     │
└─────────────────────────────────────┘
```

### Request Flow

```text
User Action
    ↓
Browser Request
    ↓
Flask Route
    ↓
Authentication / Authorization
    ↓
Input Validation
    ↓
Business Logic
    ↓
Parameterized SQL Query
    ↓
MySQL Database
    ↓
Flask Response
    ↓
Jinja2 Template
    ↓
HTML Response
    ↓
Browser
```

---

# 📁 Project Structure

```text
employee-leave-management/
│
├── app.py
│   └── Main Flask application
│       ├── Routes
│       ├── Authentication
│       ├── Authorization
│       ├── Validation
│       ├── Leave management
│       └── Dashboard logic
│
├── config.py
│   └── Loads Flask and MySQL configuration
│       from environment variables
│
├── create_admin.py
│   └── Interactive administrator account creation
│
├── requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Environment variable template
│
├── .gitignore
│   └── Files excluded from Git
│
├── database/
│   └── schema.sql
│       └── MySQL database and table definitions
│
├── templates/
│   ├── base.html
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
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

---

# 🗄️ Database Design

The application uses a MySQL database named:

```text
employee_leave_management
```

The database contains two main tables:

```text
employee_leave_management
│
├── users
│
└── leave_requests
```

---

## 👤 `users` Table

Stores employee and administrator account information.

| Column        | Type         | Description              |
| ------------- | ------------ | ------------------------ |
| `id`          | INT          | Primary key              |
| `employee_id` | VARCHAR(20)  | Unique employee/admin ID |
| `full_name`   | VARCHAR(100) | User's full name         |
| `email`       | VARCHAR(100) | Unique email address     |
| `password`    | VARCHAR(255) | Hashed password          |
| `department`  | VARCHAR(50)  | Department               |
| `role`        | ENUM         | `employee` or `admin`    |
| `created_at`  | TIMESTAMP    | Account creation time    |

---

## 📝 `leave_requests` Table

Stores all employee leave applications.

| Column          | Type         | Description                    |
| --------------- | ------------ | ------------------------------ |
| `id`            | INT          | Primary key                    |
| `user_id`       | INT          | References `users.id`          |
| `leave_type`    | ENUM         | Type of leave                  |
| `start_date`    | DATE         | Leave start date               |
| `end_date`      | DATE         | Leave end date                 |
| `reason`        | VARCHAR(500) | Employee's leave reason        |
| `status`        | ENUM         | Pending, Approved, or Rejected |
| `admin_comment` | VARCHAR(500) | Administrator comment          |
| `created_at`    | TIMESTAMP    | Request creation time          |
| `updated_at`    | TIMESTAMP    | Last update time               |

### Relationship

```text
users
  │
  │ 1
  │
  │
  │ N
  ▼
leave_requests
```

One user can have multiple leave requests.

The relationship is enforced using a foreign key:

```text
leave_requests.user_id
        ↓
users.id
```

The database uses:

```text
ON DELETE CASCADE
ON UPDATE CASCADE
```

---

# 🔐 Security

Security is an important part of the application.

## Password Hashing

Passwords are never stored as plain text.

The application uses Werkzeug:

```python
generate_password_hash()
check_password_hash()
```

During registration:

```text
Plain Password
      ↓
generate_password_hash()
      ↓
Hashed Password
      ↓
MySQL
```

During login:

```text
Entered Password
      ↓
check_password_hash()
      ↓
Authentication Result
```

---

## Session-Based Authentication

Flask sessions are used to maintain authenticated users.

The application stores information such as:

```text
user_id
full_name
role
employee_id
```

The session is cleared when the user logs out.

---

## Role-Based Authorization

The application uses separate decorators for protected routes:

```python
@login_required
@employee_required
@admin_required
```

This prevents unauthorized users from accessing restricted pages.

For example:

```text
Employee
   │
   ├── Employee Dashboard ✅
   ├── Apply Leave ✅
   ├── My Leaves ✅
   ├── Profile ✅
   └── Admin Dashboard ❌

Administrator
   │
   ├── Admin Dashboard ✅
   ├── Leave Requests ✅
   ├── Employees ✅
   └── Employee-only routes ❌
```

---

## Parameterized SQL Queries

Database queries use parameterized statements instead of string concatenation.

Example:

```python
cursor.execute(
    "SELECT id FROM users WHERE email = %s",
    (email,)
)
```

This helps protect the application against SQL injection.

---

## Server-Side Business Rules

Important business rules are enforced by the Flask backend rather than relying only on frontend validation.

For example:

* Employees cannot register themselves as administrators.
* Duplicate email addresses are rejected.
* Duplicate employee IDs are rejected.
* Invalid departments are rejected.
* Passwords must meet the minimum length requirement.
* Password confirmation must match.
* Only valid leave types are accepted.
* Leave dates are validated.
* Leave reasons have a maximum length.
* Only pending requests can be cancelled.
* Rejecting a leave request requires an administrator comment.

---

# ✅ Validation and Business Rules

## Employee Registration

The following validations are applied:

* All required fields must be completed.
* Email must have a valid format.
* Password must contain at least 6 characters.
* Password confirmation must match.
* Department must be selected from the allowed departments.
* Email must be unique.
* Employee ID must be unique.

---

## Leave Application

Supported leave types:

```text
Casual Leave
Sick Leave
Earned Leave
Emergency Leave
Unpaid Leave
```

Leave requests include:

```text
Leave Type
Start Date
End Date
Reason
```

The application calculates the number of leave days inclusively.

For example:

```text
Start Date: 10 August
End Date:   12 August

Total Leave Days = 3
```

---

## Leave Cancellation

Employees can cancel only:

```text
Pending
```

leave requests.

Once a request has been:

```text
Approved
```

or

```text
Rejected
```

it cannot be cancelled by the employee.

---

## Administrator Approval

Administrators can:

```text
Pending
   │
   ├── Approve
   │      └── Optional comment
   │
   └── Reject
          └── Required comment
```

---

# 📋 Prerequisites

Before running the project, install the following:

* Python **3.9 or higher**
* MySQL Server
* MySQL Workbench *(recommended but optional)*
* pip
* Visual Studio Code *(recommended)*
* Git *(optional)*

Verify Python:

```bash
python --version
```

Verify pip:

```bash
pip --version
```

Verify MySQL:

```bash
mysql --version
```

---

# 🚀 Installation and Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd employee-leave-management
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

After activation, your terminal should display something similar to:

```text
(venv)
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses:

```text
Flask==3.0.3
mysql-connector-python==8.4.0
python-dotenv==1.0.1
```

---

# 🗄️ MySQL Database Setup

## 1. Start MySQL

Make sure your MySQL server is running.

### Windows

You can start MySQL through:

```text
Services → MySQL
```

or through MySQL Workbench.

---

## 2. Open MySQL

Using the MySQL command line:

```bash
mysql -u root -p
```

Enter your MySQL password.

---

## 3. Execute the Schema

Inside the MySQL prompt:

```sql
SOURCE database/schema.sql;
```

The schema automatically creates:

```text
employee_leave_management
```

and the required tables:

```text
users
leave_requests
```

---

## Alternative: MySQL Workbench

1. Open MySQL Workbench.
2. Connect to your MySQL server.
3. Open:

```text
database/schema.sql
```

4. Click the **Execute** button.
5. Confirm that the database and tables were created.

---

# ⚙️ Environment Configuration

The application uses environment variables for database credentials and the Flask secret key.

Create a `.env` file in the project root.

### Windows

```bash
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Open `.env` and configure:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DB=employee_leave_management
SECRET_KEY=YOUR_SECRET_KEY
```

Replace:

```text
YOUR_PASSWORD
```

with your MySQL password.

---

## 🔑 Generate a Strong Secret Key

Run:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Example output:

```text
a1b2c3d4e5f6...
```

Copy the generated value into:

```env
SECRET_KEY=YOUR_GENERATED_SECRET_KEY
```

> **Important:** Never commit your real `.env` file or database credentials to GitHub.

---

# 👨‍💼 Creating an Administrator

Administrator accounts are created using the provided script.

Make sure:

* MySQL is running.
* The database exists.
* `.env` is configured.
* The virtual environment is activated.

Run:

```bash
python create_admin.py
```

The script asks for:

```text
Admin ID
Full Name
Email
Password
Confirm Password
```

Example:

```text
============================================================
 Employee Leave Management System - Create Administrator
============================================================

Admin ID (e.g. ADMIN001): ADMIN001
Full Name: System Administrator
Email: admin@example.com
Password (min 6 characters):
Confirm Password:
```

The password is hashed before being stored.

After successful creation:

```text
Administrator account created successfully!
```

You can then use the administrator credentials to log in.

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run on:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🪟 Windows / VS Code Quick Start

For Windows users, the complete process is:

```bash
# 1. Open the project in VS Code

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
copy .env.example .env

# 6. Configure .env with MySQL credentials

# 7. Start MySQL

# 8. Open MySQL
mysql -u root -p

# 9. Create database and tables
SOURCE database/schema.sql;

# 10. Create administrator
python create_admin.py

# 11. Run Flask application
python app.py

# 12. Open in browser
http://127.0.0.1:5000
```

---

# 👨‍💻 Employee Guide

## Step 1 — Register

Open:

```text
http://127.0.0.1:5000/register
```

Provide:

* Full Name
* Email
* Password
* Confirm Password
* Department
* Employee ID

After successful registration, log in.

---

## Step 2 — Login

Open:

```text
http://127.0.0.1:5000/login
```

Enter your registered email and password.

---

## Step 3 — Employee Dashboard

After login, the employee is redirected to the Employee Dashboard.

The dashboard displays:

```text
Total Requests
Pending Requests
Approved Requests
Rejected Requests
```

It also displays recent leave requests.

---

## Step 4 — Apply for Leave

Select:

```text
Apply Leave
```

Provide:

* Leave Type
* Start Date
* End Date
* Reason

Submit the application.

The initial status is:

```text
Pending
```

---

## Step 5 — Track Leave Requests

Open:

```text
My Leave Requests
```

Employees can view:

* Leave type
* Start date
* End date
* Number of days
* Reason
* Status
* Administrator comment

---

## Step 6 — Cancel Pending Leave

If the leave request is still:

```text
Pending
```

the employee can cancel it.

Approved and rejected requests cannot be cancelled.

---

## Step 7 — Update Profile

Employees can update:

```text
Full Name
Department
```

through the Profile page.

---

# 🛡️ Administrator Guide

## Step 1 — Create Admin Account

Run:

```bash
python create_admin.py
```

---

## Step 2 — Login

Open:

```text
http://127.0.0.1:5000/login
```

Enter the administrator credentials.

---

## Step 3 — Admin Dashboard

The administrator dashboard provides company-wide leave statistics.

It provides an overview of leave activity across employees.

---

## Step 4 — Manage Leave Requests

Open:

```text
Leave Requests
```

Administrators can review:

* Employee name
* Department
* Leave type
* Start date
* End date
* Duration
* Reason
* Status

---

## Step 5 — Filter Requests

Leave requests can be filtered by:

```text
Status
Department
```

This makes it easier to locate specific requests.

---

## Step 6 — Approve or Reject

Administrators can:

```text
Approve
```

or:

```text
Reject
```

a pending leave request.

When approving:

```text
Comment → Optional
```

When rejecting:

```text
Comment → Required
```

---

## Step 7 — View Employees

The Employees section provides a list of registered employees and their leave counts.

Administrators can view employee information including:

* Employee ID
* Name
* Email
* Department
* Leave statistics

---

# 🌐 Application Routes

## Public Routes

| Method     | Route       | Description                                     |
| ---------- | ----------- | ----------------------------------------------- |
| `GET`      | `/`         | Redirects user based on authentication and role |
| `GET/POST` | `/login`    | User login                                      |
| `GET/POST` | `/register` | Employee registration                           |
| `GET`      | `/logout`   | Logout current user                             |

---

## Employee Routes

| Method     | Route                       | Description             |
| ---------- | --------------------------- | ----------------------- |
| `GET`      | `/employee/dashboard`       | Employee dashboard      |
| `GET/POST` | `/employee/apply-leave`     | Apply for leave         |
| `GET`      | `/employee/leaves`          | View leave history      |
| `POST`     | Employee cancellation route | Cancel pending leave    |
| `GET/POST` | `/employee/profile`         | Manage employee profile |

---

## Administrator Routes

| Method | Route                        | Description                |
| ------ | ---------------------------- | -------------------------- |
| `GET`  | `/admin/dashboard`           | Administrator dashboard    |
| `GET`  | Admin leave management route | View/filter leave requests |
| `POST` | Admin approval route         | Approve leave              |
| `POST` | Admin rejection route        | Reject leave               |
| `GET`  | Admin employee route         | View employees             |

> Route names may be extended or changed during future development. The Flask source code in `app.py` is the definitive reference for the current implementation.

---

# 🗃️ Database Schema

The database is created using:

```text
database/schema.sql
```

The schema contains:

```sql
CREATE DATABASE IF NOT EXISTS employee_leave_management;
```

### Users

```text
users
├── id
├── employee_id
├── full_name
├── email
├── password
├── department
├── role
└── created_at
```

### Leave Requests

```text
leave_requests
├── id
├── user_id
├── leave_type
├── start_date
├── end_date
├── reason
├── status
├── admin_comment
├── created_at
└── updated_at
```

---

# ⚠️ Error Handling

The application includes dedicated error pages:

```text
403.html
404.html
500.html
```

These correspond to:

| Error | Meaning                         |
| ----- | ------------------------------- |
| `403` | Forbidden / unauthorized access |
| `404` | Requested page not found        |
| `500` | Internal server error           |

Database-related errors are also handled and displayed using Flask flash messages.

---

# 🧪 Troubleshooting

## MySQL Connection Refused

Make sure MySQL is running.

Check:

```text
MYSQL_HOST
MYSQL_PORT
```

in `.env`.

Default configuration:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

---

## Access Denied for MySQL User

Check:

```env
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
```

Make sure the credentials are correct.

Test the credentials:

```bash
mysql -u root -p
```

---

## Unknown Database

If you see:

```text
Unknown database 'employee_leave_management'
```

execute:

```sql
SOURCE database/schema.sql;
```

---

## `ModuleNotFoundError`

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Port Already in Use

If port `5000` is already being used, run Flask on another port.

For example:

```bash
flask --app app run --port 5001
```

Then open:

```text
http://127.0.0.1:5001
```

---

## `.env` Not Working

Make sure the file is located in the project root:

```text
employee-leave-management/
├── app.py
├── config.py
├── .env
└── ...
```

Check that the values are correctly formatted:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=employee_leave_management
SECRET_KEY=your_secret_key
```

---

## Virtual Environment Not Activated

Your terminal should show:

```text
(venv)
```

If not, activate it again.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

# 🔮 Future Enhancements

The current version provides the core employee leave management functionality. Potential future improvements include:

* Email notifications for leave status changes
* Password reset functionality
* Email verification
* Pagination for large leave-request datasets
* Advanced leave balance management
* Annual leave quotas
* Holiday calendar integration
* Leave conflict detection
* Admin account management
* Employee account deactivation
* Audit logs
* Export leave reports to CSV/PDF
* REST API integration
* Automated testing with `pytest`
* Deployment with production WSGI server
* Production database hosting
* Dashboard charts and analytics
* Improved CSRF protection
* API-based frontend integration

---

# 🎓 Learning Outcomes

This project demonstrates practical knowledge of:

### Python

* Functions
* Decorators
* Exception handling
* Regular expressions
* Date calculations
* Environment configuration
* Modular application design

### Flask

* Routing
* Request handling
* Templates
* Jinja2
* Sessions
* Flash messages
* Authentication
* Authorization
* Custom decorators
* Error handling

### MySQL

* Database creation
* Table design
* Primary keys
* Foreign keys
* ENUM fields
* Constraints
* Indexes
* CRUD operations
* Parameterized SQL queries
* Relational database design

### Web Development

* HTML5
* CSS3
* Responsive UI structure
* JavaScript
* Server-rendered applications
* Form handling
* Client/server validation

### Security

* Password hashing
* Session-based authentication
* Role-based authorization
* SQL injection prevention
* Server-side business-rule enforcement
* Environment-based secret management

---

# 🤝 Contributing

Contributions are welcome.

To contribute:

```bash
# Fork the repository

# Clone your fork
git clone <your-fork-url>

# Create a feature branch
git checkout -b feature/your-feature

# Make your changes

# Commit your changes
git add .
git commit -m "Add your feature"

# Push the branch
git push origin feature/your-feature
```

Then create a Pull Request.

---

# 📄 License

This project is available for educational and portfolio purposes.

If you intend to use, modify, or distribute the project commercially, add an appropriate license such as the MIT License.

---

# 👨‍💻 Author

## Mayank Singh Negi

**B.Tech — Computer Science and Engineering**

Faridabad, Haryana, India

### Connect With Me

* **GitHub:** [github.com/mayanksnegi](https://github.com/mayanksnegi)
* **LinkedIn:** [linkedin.com/in/mayanksnegi](https://linkedin.com/in/mayanksnegi)
* **Portfolio:** [mayanksnegi-portfolio.netlify.app](https://mayanksnegi-portfolio.netlify.app)

---

# ⭐ Project Highlights

```text
┌──────────────────────────────────────────────┐
│       EMPLOYEE LEAVE MANAGEMENT SYSTEM       │
├──────────────────────────────────────────────┤
│                                              │
│  🐍 Python + Flask                           │
│  🗄️ MySQL Database                           │
│  🎨 HTML + CSS + JavaScript                  │
│  🔐 Secure Password Hashing                  │
│  👥 Role-Based Authentication                │
│  📝 Leave Application Management             │
│  ✅ Admin Approval / Rejection               │
│  📊 Employee & Admin Dashboards              │
│  🔎 Leave Filtering                          │
│  🛡️ Parameterized SQL Queries                │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

For experienced users, the complete setup can be summarized as:

```bash
# Clone
git clone <repository-url>
cd employee-leave-management

# Virtual environment
python -m venv venv
venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment
copy .env.example .env

# Configure .env

# Database
mysql -u root -p
SOURCE database/schema.sql;

# Administrator
python create_admin.py

# Run
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## ⭐ If You Like This Project

If this project helped you or you found it useful, consider giving the repository a ⭐ on GitHub.
