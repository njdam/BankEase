#!/usr/bin/python3

import mysql.connector


connection = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="   ",
        database="BankEase",
        )

cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(250) UNIQUE NOT NULL,
        password VARCHAR(250) NOT NULL,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        country VARCHAR(255),
        city VARCHAR(255),
        home_address VARCHAR(255),
        is_admin BOOLEAN DEFAULT FALSE, -- Customer or Admin
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''', multi=True)

cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
        account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        account_type VARCHAR(50) NOT NULL, -- e.g., savings, checking
        balance DECIMAL(10, 2) DEFAULT 0.00,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ) AUTO_INCREMENT = 970321240000; -- Set the initial value to start
        ''', multi=True)

cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        account_number BIGINT NOT NULL,
        type VARCHAR(250) NOT NULL, -- e.g., deposit, withdrawal, transfer
        amount DECIMAL(10, 2) NOT NULL,
        balance DECIMAL(10, 2) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        );
        ''', multi=True)

cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
        loan_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        interest_rate DECIMAL(5, 2) NOT NULL,
        term_months INT NOT NULL,
        status VARCHAR(50) NOT NULL, -- e.g., pending, approved, rejected
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        ''', multi=True)

cursor.close()
connection.close()
