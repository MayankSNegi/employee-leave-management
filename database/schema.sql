-- =====================================================================
-- Employee Leave Management System - Database Schema
-- =====================================================================
-- Run this file to create the database and all required tables.
--
-- Command line:
--   mysql -u root -p
--   SOURCE database/schema.sql;
--
-- MySQL Workbench:
--   Open this file and click "Execute".
-- =====================================================================

CREATE DATABASE IF NOT EXISTS employee_leave_management;

USE employee_leave_management;

-- ---------------------------------------------------------------------
-- Table: users
-- Stores both employee and administrator accounts.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    employee_id   VARCHAR(20)  NOT NULL UNIQUE,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    department    VARCHAR(50)  NOT NULL,
    role          ENUM('employee', 'admin') NOT NULL DEFAULT 'employee',
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- Table: leave_requests
-- Stores every leave application submitted by employees.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS leave_requests (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    leave_type     ENUM('Casual Leave', 'Sick Leave', 'Earned Leave',
                         'Emergency Leave', 'Unpaid Leave') NOT NULL,
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL,
    reason         VARCHAR(500) NOT NULL,
    status         ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    admin_comment  VARCHAR(500) DEFAULT NULL,
    created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_leave_requests_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_leave_requests_user_id (user_id),
    INDEX idx_leave_requests_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
