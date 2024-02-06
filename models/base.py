#!/usr/bin/python3
""" A file which deal with BankEase basic prototype. """

import json
import bcrypt
import mysql.connector


class BankEase:
    """ BankEase System Tools. """
    connection = None

    @classmethod
    def connect(cls):
        cls.connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="   ",
            database="BankEase"
        )

    @classmethod
    def disconnect(cls):
        if cls.connection:
            cls.connection.close()

    @classmethod
    def execute_query(cls, query, values=None, multi=False):
        if cls.connection is None:
            cls.connect()
        try:
            with cls.connection.cursor(dictionary=True) as cursor:
                if multi:
                    cursor.execute(query, multi=True)
                else:
                    cursor.execute(query, values)
                    result = cursor.fetchall()

            if not multi:
                cls.connection.commit()
                cursor.close()
                json_str = json.dumps(result, default=str)
                return json.loads(json_str)  # Convert result to JSON Data

        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_valid_username():
        """ Function to get valid username """
        while True:
            username = input("Enter username: ")
            if len(username) >= 6:
                return username
            else:
                print("Username must be at least 6 characters. Try again.")

    def get_valid_password():
        """" Function to get valid password """
        while True:
            password = input("Enter password: ")
            if len(password) >= 6:
                return password
            else:
                print("Password must be at least 6 characters. Try again.")

    def get_valid_phone_number():
        """ Function to get valid phone number """
        while True:
            phone_number = input("Enter phone number: ")
            if len(phone_number) >= 10:
                return phone_number
            else:
                print("At least 10 characters. Try again.")

    @staticmethod
    def hash_password(password):
        """Hash the password using bcrypt."""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash

    @staticmethod
    def check_password(password, stored_password):
        """
        Check if the provided password matches the stored hashed password.
        """
        encoded_password = password.encode('utf-8')
        encoded_stored = stored_password.encode('utf-8')

        return bcrypt.checkpw(encoded_password, encoded_stored)

    '''
    @staticmethod
    def load_recipient(username):
        users = BankEase.load_users()
        for user in users:
            if user['username'] == username:
                user_instance = BankEase(username, "")
                user_instance.id = user["id"]
                user_instance.account_number = user["account_number"]
                user_instance.balance = user["balance"]
                user_instance.transaction_history = user["transaction_history"]
                return user_instance
        return None

    @staticmethod
    def load_user_by_username(username):
        users = BankEase.load_users()
        for user in users:
            if user['username'] == username:
                return user
        return None

    @staticmethod
    def load_users():
        """A function to return all saved users in json format."""
        users = []
        try:
            with open("user_data.json", "r") as file:
                lines = file.readlines()
                for line in lines:
                    user_info = json.loads(line)
                    users.append(user_info)

        except FileNotFoundError:
            pass

        return users'''
