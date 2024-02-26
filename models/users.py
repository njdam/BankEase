#!/usr/bin/python3

from models.base import BankEase
from models.accounts import Account
from models.loans import Loan
import mysql.connector
import json
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from api.v1.app import db, login_manager


class User(db.Model, UserMixin, BankEase):
    """A function which create a user for BankEase System."""
    __tablename__ = 'users'  # Specify the table name explicitly
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    home_address = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    accounts = db.relationship('Account', backref='user', lazy=True)
    loans = db.relationship('Loan', backref='user', lazy=True)

    def __init__(self, username, password):
        """ User initialisation """
        self.username = username
        self.password = self.hash_password(password)
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone_number = None
        self.country = None
        self.city = None
        self.home_address = None
        self.is_admin = False
        self.created_at = None
        super(User, self).__init__() # Call the constructor of db.Model

    @staticmethod
    def username_exists(username):
        user_info = User.get_user_by_username(username)
        if user_info:
            return 1
        else:
            return 0

    @property
    def is_active(self):
        return True

    def get_id(self):
        """Return the user's ID as a unicode string."""
        return str(self.user_id)

    def get_account(self):
        """ Get the associated account for this user. """
        if not isinstance(self, AnonymousUserMixin):
            query = 'SELECT * FROM accounts WHERE user_id = %s'
            if hasattr(self, 'user_id') and self.user_id is not None:
                values = (self.user_id,)
                account_info = self.execute_query(query, values)
                if account_info:
                    account_data = account_info[0]
                    account_instance = Account(user_id=account_data['user_id'])
                    # Set attributes for the Account instance
                    for key, value in account_data.items():
                        setattr(account_instance, key, value)
                    return account_instance
                else:
                    pass
            else:
                pass
        else:
            pass

    def get_loans(self):
        """ Get the associated loans for this user. """
        if not isinstance(self, AnonymousUserMixin):
            query = 'SELECT * FROM loans WHERE user_id = %s'
            if hasattr(self, 'user_id') and self.user_id is not None:
                values = (self.user_id,)
                loan_info = self.execute_query(query, values)
                if loan_info:
                    return loan_info
                else:
                    return None
            else:
                pass
        else:
            pass

    @classmethod
    def signin(cls, username, password):
        """ Signin for accessing user information. """
        while True:
            try:
                user = cls.authenticate(username, password)
                return user
            except AuthenticationError as e:
                print(f"{e} Please try again!")

    @classmethod
    def signup(
            cls, username, password, first_name, last_name,
            email, phone_number,
            country, city, home_address, account_type
            ):
        """ Input of user information to create new user. """
        while True:
            try:
                cls.create_user(
                    username, password, first_name, last_name,
                    email, phone_number,
                    country, city, home_address, account_type
                    )

                print("Account created successfully!")
                return (1)
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate entry error
                    print(f"Error: Username '{username}' already exists. Please choose a different username.")
                    exit()
                else:
                    print(f"Error: {err}")
                    exit()
            except Exception as e:
                print(f"Error: {e}")
                exit()

    @classmethod
    def authenticate(cls, username, password):
        """Sign in function"""
        try:
            user_info = cls.get_user_by_username(username)
            user_data = user_info[0]
            if user_info and cls.check_password(password, user_data["password"]):
                user_instance = cls(username, password)
                for key, value in user_data.items():
                    setattr(user_instance, key, value)
                return user_instance
            else:
                raise AuthenticationError("Invalid username or password!!")

        except Exception as e:
            print(f"Error: {e}")
    
    @classmethod
    def create_user(cls, username, password, first_name, last_name, email, phone_number, country, city, home_address, account_type, is_admin=False):
        """ A function to create a new user account. """
        hash_password = cls.hash_password(password)

        query = '''
        CREATE DATABASE IF NOT EXISTS BankEase;
        '''
        cls.execute_query(query, multi=True)

        query = '''
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
        )
        '''
        cls.execute_query(query, multi=True)

        query = '''
        INSERT INTO users (username, password, first_name, last_name, email, phone_number, country, city, home_address, is_admin)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
                username, hash_password, first_name, last_name,
                email, phone_number, country, city, home_address,
                is_admin)
        cls.execute_query(query, values)

        # Setting a new created account's user instances
        user_info = cls.get_user_by_username(username)
        if user_info:
            user_data = user_info[0]
            user_instance = cls(username, password)
            for key, value in user_data.items():
                setattr(user_instance, key, value)
        else:
            raise Exception("Failed to set User atrributes.")
            
        Account.create_account(user_data["user_id"], account_type)

    @classmethod
    def get_user_by_username(cls, username):
        query = 'SELECT * FROM users WHERE username = %s'
        values = (username,)
        result = cls.execute_query(query, values)
        return result


class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass
