#!/usr/bin/python3
""" Base Model file for handling creation of new users """

import json
import bcrypt
from datetime import datetime
from models.engine.db_bankease import DB_BankEase


class BankEase:
    """Create NewUser"""
    latest_id = 0
    account_number = 100010001000

    def __init__(self, username, password):
        """Initialisation of user account of bank account."""
        self.load_latest_id()
        BankEase.latest_id += 1
        self.id = BankEase.latest_id
        self.account_number = BankEase.account_number + BankEase.latest_id
        self.username = username
        self.password = self.hash_password(password)
        self.balance = 0
        self.deposited_at = None
        self.withdrawn_at = None
        self.transferred_at = None
        self.transaction_history = None

    def load_latest_id(self):
        data = self.load_users()
        if data:
            max_id = max(user["id"] for user in data)
            BankEase.latest_id = max_id
        else:
            pass

    def hash_password(self, password):
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

    def deposit(self, amount):
        """A function to deposit amount of money."""
        amount = int(amount)
        self.balance += amount
        self.deposited_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Update transaction history
        transaction = {'type': 'deposit', 'amount': amount, 'balance': self.balance, 'timestamp': self.deposited_at}
        self.transaction_history = transaction
        # save updated user information
        self.save_update()
        print(f"Deposited ${amount} at {self.deposited_at}.")
        print(f"Current Balance: ${self.balance}")

    def withdraw(self, amount):
        """A function to withdraw amount of money."""
        amount = int(amount)
        if amount <= self.balance:
            self.balance -= amount
            self.withdrawn_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction = {'type': 'withdraw', 'amount': amount, 'balance': self.balance, 'timestamp': self.withdrawn_at}
            self.transaction_history = transaction
            self.save_update()
            print(f"Withdrew ${amount} at {self.withdrawn_at}.")
            print(f"Current Balance: ${self.balance}")
        else:
            print("Insufficient funds!")

    def transfer(self, username, amount):
        """A function to transfer amount of money to another user."""
        recipient = self.load_recipient(username)
        amount = int(amount)
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transferred_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sender = {'type': 'transfer', 'amount': amount, 'balance': self.balance, 'timestamp': self.transferred_at}
            self.transaction_history = sender
            self.save_update()
            receiver = {'type': 'received', 'amount': amount, 'balance': recipient.balance, 'timestamp': self.transferred_at}
            recipient.transaction_history = receiver
            recipient.save_update()

            print(f"Transferred ${amount} to {recipient.username}\
                    at {self.transferred_at}.")
            print(f"Your Current Balance: ${self.balance}")

        else:
            print("Insufficient funds!")

    def get_balance(self):
        """A function to return a balance on account."""
        return self.balance

    # Function to get valid username
    def get_valid_username():
        while True:
            username = input("Enter username: ")
            if len(username) >= 6:
                return username
            else:
                print("Username must be at least 6 characters. Try again.")

    # Function to get valid password
    def get_valid_password():
        while True:
            password = input("Enter password: ")
            if len(password) >= 6:
                return password
            else:
                print("Password must be at least 6 characters. Try again.")

    # Function to get valid phone number
    def get_valid_phone_number():
        while True:
            phone_number = input("Enter phone number: ")
            if len(phone_number) >= 10:
                return phone_number
            else:
                print("At least 10 characters. Try again.")

    def save_update(self):
        """Save the user's information to storage (e.g., JSON file)."""
        DB_BankEase.save_update(self)
        '''
        # Retrieve existing user data
        users = self.load_users()

        # Find the user's data in the list and update it
        for user_data in users:
            if user_data["id"] == self.id:
                user_data["balance"] = self.balance
                user_data["transaction_history"].append(self.transaction_history)

        # Save the updated user data back to storage
        with open("user_data.json", "w") as file:
            for user_data in users:
                json.dump(user_data, file)
                file.write("\n")'''

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

        return users
