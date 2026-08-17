"""
config.py

Central configuration for the Employee Leave Management System.
Values are loaded from environment variables (see .env.example).
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv()


class Config:
    # Flask secret key (used for sessions, flash messages, CSRF protection, etc.)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

    # MySQL connection settings
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "employee_leave_management")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
