#!/usr/bin/python3
# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error
from datetime import datetime

# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(20))
    country = Column(String(255))
    city = Column(String(255))
    home_address = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship('Account', back_populates='user')
    loans = relationship('Loan', back_populates='user')

class Account(Base):
    __tablename__ = 'accounts'

    account_number = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    account_type = Column(String(50), nullable=False)
    balance = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_number = Column(Integer, ForeignKey('accounts.account_number'), nullable=False)
    type = Column(String(250), nullable=False)
    amount = Column(DECIMAL(10, 2))
    balance = Column(DECIMAL(10, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)

    account = relationship('Account', back_populates='transactions')

class Loan(Base):
    __tablename__ = 'loans'

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    amount = Column(DECIMAL(10, 2))
    interest_rate = Column(DECIMAL(5, 2))
    term_months = Column(Integer)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='loans')

# Database initialization and session creation
engine = create_engine('sqlite:///bankease.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Example usage:
# Create a new user
new_user = User(username='john_doe', password='password', first_name='John', last_name='Doe', email='john@example.com')
session.add(new_user)
session.commit()

# Create a new account for the user
new_account = Account(user=new_user, account_type='savings')
session.add(new_account)
session.commit()

# Create a new transaction for the account
new_transaction = Transaction(account=new_account, type='deposit', amount=1000, balance=1000)
session.add(new_transaction)
session.commit()


class DatabaseHandler:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host="your_mysql_host",
                user="your_mysql_user",
                password="your_mysql_password",
                database="your_database_name",
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")

        except Error as e:
            print(f"Error: {e}")

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

    def create_user_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(250) UNIQUE NOT NULL,
                password VARCHAR(250) NOT NULL,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                email VARCHAR(255),
                phone_number VARCHAR(20),
                country VARCHAR(255),
                city VARCHAR(255),
                home_address VARCHAR(255),
                is_admin BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.execute_query(query)

    def create_accounts_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                account_type VARCHAR(50),
                balance DECIMAL(10, 2) DEFAULT 0.00,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE (`account_number`)
            )
        '''
        self.execute_query(query)

    def create_transactions_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                account_number BIGINT,
                type VARCHAR(250),
                amount DECIMAL(10, 2),
                balance DECIMAL(10, 2),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        '''
        self.execute_query(query)

    def create_loans_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                amount DECIMAL(10, 2),
                interest_rate DECIMAL(5, 2),
                term_months INT,
                status VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        '''
        self.execute_query(query)

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: {e}")

# Example usage:
db_handler = DatabaseHandler()
db_handler.create_user_table()
db_handler.create_accounts_table()
db_handler.create_transactions_table()
db_handler.create_loans_table()
