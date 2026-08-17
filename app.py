"""
app.py

Employee Leave Management System
A full-stack Flask + MySQL web application that allows employees to
register, log in, apply for leave, and track leave status, while
administrators can review employees and approve/reject leave requests.
"""

import re
from datetime import datetime, date
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error as MySQLError

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEPARTMENTS = ["Engineering", "Human Resources", "Finance",
               "Marketing", "Sales", "Operations", "IT"]
LEAVE_TYPES = ["Casual Leave", "Sick Leave", "Earned Leave",
               "Emergency Leave", "Unpaid Leave"]
MAX_REASON_LENGTH = 500


# ---------------------------------------------------------------------
# Database helper
# ---------------------------------------------------------------------
def get_db_connection():
    """Create and return a new MySQL connection using dictionary cursors."""
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DB"],
    )


# ---------------------------------------------------------------------
# Authentication / Authorization helpers
# ---------------------------------------------------------------------
def login_required(f):
    """Ensure the user is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Ensure the logged-in user has the 'admin' role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("You are not authorized to access this page.", "error")
            return redirect(url_for("employee_dashboard"))
        return f(*args, **kwargs)
    return decorated_function


def employee_required(f):
    """Ensure the logged-in user has the 'employee' role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "employee":
            flash("You are not authorized to access this page.", "error")
            return redirect(url_for("admin_dashboard"))
        return f(*args, **kwargs)
    return decorated_function


def calculate_days(start_date, end_date):
    """Inclusive number of days between two date objects."""
    return (end_date - start_date).days + 1


# ---------------------------------------------------------------------
# Home route - smart redirect
# ---------------------------------------------------------------------
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("employee_dashboard"))


# ---------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        department = request.form.get("department", "").strip()
        employee_id = request.form.get("employee_id", "").strip()

        form_data = {
            "full_name": full_name,
            "email": email,
            "department": department,
            "employee_id": employee_id,
        }

        # --- Validation ---
        if not all([full_name, email, password, confirm_password,
                    department, employee_id]):
            flash("All fields are required.", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)

        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)

        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)

        if department not in DEPARTMENTS:
            flash("Please select a valid department.", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("An account with this email already exists.", "error")
                cursor.close()
                return render_template("register.html", departments=DEPARTMENTS,
                                        form_data=form_data)

            cursor.execute("SELECT id FROM users WHERE employee_id = %s",
                           (employee_id,))
            if cursor.fetchone():
                flash("This Employee ID is already registered.", "error")
                cursor.close()
                return render_template("register.html", departments=DEPARTMENTS,
                                        form_data=form_data)

            hashed_password = generate_password_hash(password)

            cursor.execute(
                """INSERT INTO users
                   (employee_id, full_name, email, password, department, role)
                   VALUES (%s, %s, %s, %s, %s, 'employee')""",
                (employee_id, full_name, email, hashed_password, department)
            )
            conn.commit()
            cursor.close()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        except MySQLError as err:
            flash(f"Database error: {err}", "error")
            return render_template("register.html", departments=DEPARTMENTS,
                                    form_data=form_data)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    return render_template("register.html", departments=DEPARTMENTS, form_data={})


# ---------------------------------------------------------------------
# Login / Logout
# ---------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html", email=email)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["full_name"] = user["full_name"]
                session["role"] = user["role"]
                session["employee_id"] = user["employee_id"]

                flash(f"Welcome back, {user['full_name']}!", "success")

                if user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                return redirect(url_for("employee_dashboard"))

            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email)

        except MySQLError as err:
            flash(f"Database error: {err}", "error")
            return render_template("login.html", email=email)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    return render_template("login.html", email="")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------
# Employee Dashboard
# ---------------------------------------------------------------------
@app.route("/employee/dashboard")
@employee_required
def employee_dashboard():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_id = session["user_id"]

        cursor.execute(
            """SELECT
                   COUNT(*) AS total,
                   SUM(status = 'Pending')  AS pending,
                   SUM(status = 'Approved') AS approved,
                   SUM(status = 'Rejected') AS rejected
               FROM leave_requests WHERE user_id = %s""",
            (user_id,)
        )
        stats = cursor.fetchone()

        cursor.execute(
            """SELECT * FROM leave_requests
               WHERE user_id = %s
               ORDER BY created_at DESC LIMIT 5""",
            (user_id,)
        )
        recent_leaves = cursor.fetchall()
        cursor.close()

        for leave in recent_leaves:
            leave["num_days"] = calculate_days(leave["start_date"], leave["end_date"])

        stats = {
            "total": stats["total"] or 0,
            "pending": stats["pending"] or 0,
            "approved": stats["approved"] or 0,
            "rejected": stats["rejected"] or 0,
        }

        return render_template("employee_dashboard.html",
                                stats=stats, recent_leaves=recent_leaves)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return render_template("employee_dashboard.html",
                                stats={"total": 0, "pending": 0,
                                       "approved": 0, "rejected": 0},
                                recent_leaves=[])
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Apply for Leave
# ---------------------------------------------------------------------
@app.route("/employee/apply-leave", methods=["GET", "POST"])
@employee_required
def apply_leave():
    if request.method == "POST":
        leave_type = request.form.get("leave_type", "").strip()
        start_date_str = request.form.get("start_date", "").strip()
        end_date_str = request.form.get("end_date", "").strip()
        reason = request.form.get("reason", "").strip()

        form_data = {
            "leave_type": leave_type,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "reason": reason,
        }

        if not all([leave_type, start_date_str, end_date_str, reason]):
            flash("All fields are required.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        if leave_type not in LEAVE_TYPES:
            flash("Please select a valid leave type.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        if len(reason) > MAX_REASON_LENGTH:
            flash(f"Reason must be under {MAX_REASON_LENGTH} characters.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Please provide valid dates.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        if start_date < date.today():
            flash("Start date cannot be before the current date.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        if end_date < start_date:
            flash("End date cannot be before start date.", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO leave_requests
                   (user_id, leave_type, start_date, end_date, reason, status)
                   VALUES (%s, %s, %s, %s, %s, 'Pending')""",
                (session["user_id"], leave_type, start_date, end_date, reason)
            )
            conn.commit()
            cursor.close()

            flash("Leave request submitted successfully.", "success")
            return redirect(url_for("my_leaves"))
        except MySQLError as err:
            flash(f"Database error: {err}", "error")
            return render_template("apply_leave.html", leave_types=LEAVE_TYPES,
                                    form_data=form_data)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    return render_template("apply_leave.html", leave_types=LEAVE_TYPES, form_data={})


# ---------------------------------------------------------------------
# My Leave Requests
# ---------------------------------------------------------------------
@app.route("/employee/leaves")
@employee_required
def my_leaves():
    status_filter = request.args.get("status", "All")
    valid_statuses = {"All", "Pending", "Approved", "Rejected"}
    if status_filter not in valid_statuses:
        status_filter = "All"

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if status_filter == "All":
            cursor.execute(
                """SELECT * FROM leave_requests
                   WHERE user_id = %s ORDER BY created_at DESC""",
                (session["user_id"],)
            )
        else:
            cursor.execute(
                """SELECT * FROM leave_requests
                   WHERE user_id = %s AND status = %s
                   ORDER BY created_at DESC""",
                (session["user_id"], status_filter)
            )
        leaves = cursor.fetchall()
        cursor.close()

        for leave in leaves:
            leave["num_days"] = calculate_days(leave["start_date"], leave["end_date"])

        return render_template("my_leaves.html", leaves=leaves,
                                status_filter=status_filter)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return render_template("my_leaves.html", leaves=[], status_filter=status_filter)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Cancel Leave Request
# ---------------------------------------------------------------------
@app.route("/employee/leave/<int:leave_id>/cancel", methods=["POST"])
@employee_required
def cancel_leave(leave_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM leave_requests WHERE id = %s", (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            flash("Leave request not found.", "error")
            cursor.close()
            return redirect(url_for("my_leaves"))

        if leave["user_id"] != session["user_id"]:
            flash("You are not authorized to modify this leave request.", "error")
            cursor.close()
            return redirect(url_for("my_leaves"))

        if leave["status"] != "Pending":
            flash("Only pending leave requests can be cancelled.", "error")
            cursor.close()
            return redirect(url_for("my_leaves"))

        cursor.execute("DELETE FROM leave_requests WHERE id = %s", (leave_id,))
        conn.commit()
        cursor.close()

        flash("Leave request cancelled successfully.", "success")
        return redirect(url_for("my_leaves"))
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return redirect(url_for("my_leaves"))
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Employee Profile
# ---------------------------------------------------------------------
@app.route("/employee/profile", methods=["GET", "POST"])
@employee_required
def profile():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            department = request.form.get("department", "").strip()

            if not full_name or not department:
                flash("Full name and department are required.", "error")
            elif department not in DEPARTMENTS:
                flash("Please select a valid department.", "error")
            else:
                cursor.execute(
                    "UPDATE users SET full_name = %s, department = %s WHERE id = %s",
                    (full_name, department, session["user_id"])
                )
                conn.commit()
                session["full_name"] = full_name
                flash("Profile updated successfully.", "success")

        cursor.execute("SELECT * FROM users WHERE id = %s", (session["user_id"],))
        user = cursor.fetchone()
        cursor.close()

        return render_template("profile.html", user=user, departments=DEPARTMENTS)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return redirect(url_for("employee_dashboard"))
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Admin Dashboard
# ---------------------------------------------------------------------
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_employees FROM users WHERE role = 'employee'")
        total_employees = cursor.fetchone()["total_employees"]

        cursor.execute(
            """SELECT
                   COUNT(*) AS total,
                   SUM(status = 'Pending')  AS pending,
                   SUM(status = 'Approved') AS approved,
                   SUM(status = 'Rejected') AS rejected
               FROM leave_requests"""
        )
        stats_row = cursor.fetchone()

        stats = {
            "total_employees": total_employees,
            "total": stats_row["total"] or 0,
            "pending": stats_row["pending"] or 0,
            "approved": stats_row["approved"] or 0,
            "rejected": stats_row["rejected"] or 0,
        }

        cursor.execute(
            """SELECT lr.*, u.full_name, u.employee_id, u.department
               FROM leave_requests lr
               JOIN users u ON lr.user_id = u.id
               ORDER BY lr.created_at DESC LIMIT 5"""
        )
        recent_leaves = cursor.fetchall()
        cursor.close()

        for leave in recent_leaves:
            leave["num_days"] = calculate_days(leave["start_date"], leave["end_date"])

        return render_template("admin_dashboard.html", stats=stats,
                                recent_leaves=recent_leaves)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return render_template(
            "admin_dashboard.html",
            stats={"total_employees": 0, "total": 0, "pending": 0,
                   "approved": 0, "rejected": 0},
            recent_leaves=[]
        )
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Admin - Manage Leave Requests
# ---------------------------------------------------------------------
@app.route("/admin/leaves")
@admin_required
def admin_leaves():
    status_filter = request.args.get("status", "All")
    department_filter = request.args.get("department", "All")

    valid_statuses = {"All", "Pending", "Approved", "Rejected"}
    if status_filter not in valid_statuses:
        status_filter = "All"

    if department_filter != "All" and department_filter not in DEPARTMENTS:
        department_filter = "All"

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT lr.*, u.full_name, u.employee_id, u.department
                   FROM leave_requests lr
                   JOIN users u ON lr.user_id = u.id
                   WHERE 1 = 1"""
        params = []

        if status_filter != "All":
            query += " AND lr.status = %s"
            params.append(status_filter)

        if department_filter != "All":
            query += " AND u.department = %s"
            params.append(department_filter)

        query += " ORDER BY lr.created_at DESC"

        cursor.execute(query, tuple(params))
        leaves = cursor.fetchall()
        cursor.close()

        for leave in leaves:
            leave["num_days"] = calculate_days(leave["start_date"], leave["end_date"])

        return render_template("admin_leaves.html", leaves=leaves,
                                status_filter=status_filter,
                                department_filter=department_filter,
                                departments=DEPARTMENTS)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return render_template("admin_leaves.html", leaves=[],
                                status_filter=status_filter,
                                department_filter=department_filter,
                                departments=DEPARTMENTS)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


@app.route("/admin/leave/<int:leave_id>/approve", methods=["POST"])
@admin_required
def approve_leave(leave_id):
    admin_comment = request.form.get("admin_comment", "").strip()
    return _process_leave(leave_id, "Approved", admin_comment)


@app.route("/admin/leave/<int:leave_id>/reject", methods=["POST"])
@admin_required
def reject_leave(leave_id):
    admin_comment = request.form.get("admin_comment", "").strip()
    if not admin_comment:
        flash("Please provide a reason when rejecting a leave request.", "error")
        return redirect(url_for("admin_leaves"))
    return _process_leave(leave_id, "Rejected", admin_comment)


def _process_leave(leave_id, new_status, admin_comment):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM leave_requests WHERE id = %s", (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            flash("Leave request not found.", "error")
            cursor.close()
            return redirect(url_for("admin_leaves"))

        cursor.execute(
            """UPDATE leave_requests
               SET status = %s, admin_comment = %s
               WHERE id = %s""",
            (new_status, admin_comment or None, leave_id)
        )
        conn.commit()
        cursor.close()

        flash(f"Leave request {new_status.lower()} successfully.", "success")
        return redirect(url_for("admin_leaves"))
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return redirect(url_for("admin_leaves"))
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Admin - Employee Management
# ---------------------------------------------------------------------
@app.route("/admin/employees")
@admin_required
def admin_employees():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT u.id, u.employee_id, u.full_name, u.email, u.department,
                      u.created_at, COUNT(lr.id) AS leave_count
               FROM users u
               LEFT JOIN leave_requests lr ON lr.user_id = u.id
               WHERE u.role = 'employee'
               GROUP BY u.id, u.employee_id, u.full_name, u.email,
                        u.department, u.created_at
               ORDER BY u.created_at DESC"""
        )
        employees = cursor.fetchall()
        cursor.close()

        return render_template("admin_employees.html", employees=employees)
    except MySQLError as err:
        flash(f"Database error: {err}", "error")
        return render_template("admin_employees.html", employees=[])
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


# ---------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------
@app.errorhandler(403)
def forbidden_error(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
