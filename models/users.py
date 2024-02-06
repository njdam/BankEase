#!/usr/bin/python3

from models.base import BankEase
from models.accounts import Account
from models.loans import Loan
import mysql.connector
import json


class User(Account, Loan):
    """A function which create a user for BankEase System."""

    def __init__(self, username, password):
        """ User initialisation """
        self.user_id = None
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
        super().__init__(self.user_id)

    def get_account(self):
        """ Get the associated account for this user. """
        query = 'SELECT * FROM accounts WHERE user_id = %s'
        values = (self.user_id,)  # user_id is stored in the User instance
        account_info = self.execute_query(query, values)

        if account_info:
            account_data = account_info[0]
            account_instance = Account(user_id=self.user_id)
            for key, value in account_data.items():
                setattr(account_instance, key, value)
            return account_instance
        else:
            raise Exception("No account found for this user.")

    @classmethod
    def signin(cls):
        """ Signin for accessing user information. """
        while True:
            print("Welcome to BankEase - Banking Simplified, Anytime, Anywhere")
            print("...........................................................")
            print("BankEase SingIn Page\n")
            try:
                username = cls.get_valid_username()
                password = cls.get_valid_password()
                try:
                    user = cls.authenticate(username, password)
                    return user
                except AuthenticationError as e:
                    print(f"{e} Please try again!")

            except KeyboardInterrupt:
                print("\nThank you for visiting us!")
                print("Exiting...................")
                exit()

    @classmethod
    def signup(cls):
        """ Input of user information to create new user. """
        while True:
            print("Welcome to BankEase - Banking Simplified, Anytime, Anywhere")
            print("...........................................................")
            print("BankEase SingUp Page\n")
            try:
                username = cls.get_valid_username()
                password = cls.get_valid_password()
                first_name = input("Enter Your First Name: ")
                last_name = input("Enter Your Last Name: ")
                email = input("Enter Your Email: ")
                phone_number = cls.get_valid_phone_number()
                country = input("Enter Your Country: ")
                city = input("Enter Your City: ")
                home_address = input("Enter Your Home Address: ")
                try:
                    cls.create_user_table()
                    cls.create_user(
                            username, password, first_name, last_name,
                            email, phone_number,
                            country, city, home_address
                            )
                    print("Account created successfully!")
                    break
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

            except KeyboardInterrupt:
                print("\nThank you for visiting us!")
                print("Existing .................")
                exit()

    @classmethod
    def authenticate(cls, username, password):
        """Sign in function"""
        user_info = cls.get_user_by_username(username)
        user_data = user_info[0]
        if user_info and cls.check_password(password, user_data["password"]):
            user_instance = cls(username, password)
            for key, value in user_data.items():
                setattr(user_instance, key, value)
            return user_instance
        else:
            raise AuthenticationError("Invalid username or password!!")
    
    @classmethod
    def create_user_table(cls):
        """ A function to create table users in mysql database. """
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

    @classmethod
    def create_user(cls, username, password, first_name, last_name, email, phone_number, country, city, home_address, is_admin=False):
        """ A function to create a new user account. """
        hash_password = cls.hash_password(password)

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
            
        account_type = input("Enter Account Type(Current, Saving, Fixed): ")
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
