"""
create_admin.py

Interactive script to create an Administrator account for the
Employee Leave Management System.

Usage:
    python create_admin.py

You will be prompted for the admin's Employee/Admin ID, full name,
email, and password. The password is securely hashed before being
stored in the database. Duplicate accounts (matching email or
employee ID) are rejected.
"""

import getpass
import re
import sys

import mysql.connector
from mysql.connector import Error as MySQLError
from werkzeug.security import generate_password_hash

from config import Config

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
    )


def prompt_non_empty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def prompt_email():
    while True:
        email = input("Email: ").strip().lower()
        if EMAIL_REGEX.match(email):
            return email
        print("Please enter a valid email address.")


def prompt_password():
    while True:
        password = getpass.getpass("Password (min 6 characters): ")
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        confirm = getpass.getpass("Confirm Password: ")
        if password != confirm:
            print("Passwords do not match. Please try again.")
            continue
        return password


def main():
    print("=" * 60)
    print(" Employee Leave Management System - Create Administrator")
    print("=" * 60)

    employee_id = prompt_non_empty("Admin ID (e.g. ADMIN001): ")
    full_name = prompt_non_empty("Full Name: ")
    email = prompt_email()
    password = prompt_password()

    try:
        conn = get_db_connection()
    except MySQLError as err:
        print(f"\nCould not connect to the database: {err}")
        print("Check your .env configuration and ensure MySQL is running.")
        sys.exit(1)

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"\nAn account with email '{email}' already exists.")
            sys.exit(1)

        cursor.execute("SELECT id FROM users WHERE employee_id = %s", (employee_id,))
        if cursor.fetchone():
            print(f"\nAn account with Admin ID '{employee_id}' already exists.")
            sys.exit(1)

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """INSERT INTO users
               (employee_id, full_name, email, password, department, role)
               VALUES (%s, %s, %s, %s, %s, 'admin')""",
            (employee_id, full_name, email, hashed_password, "Administration")
        )
        conn.commit()
        cursor.close()

        print("\nAdministrator account created successfully!")
        print(f"  Admin ID : {employee_id}")
        print(f"  Name     : {full_name}")
        print(f"  Email    : {email}")
        print("\nYou can now log in at http://127.0.0.1:5000/login")

    except MySQLError as err:
        print(f"\nDatabase error: {err}")
        sys.exit(1)
    finally:
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
