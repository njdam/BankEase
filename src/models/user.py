#!/usr/bin/python3
""" Base Model file for handling creation of new users """

import json
from datetime import datetime
from models.base import BankEase


class User(BankEase):
    """Create NewUser"""

    def __init__(self, username, password):
        """Initialisation of user account of bank account."""
        super().__init__(username, password)
        self.created_at = None

    @classmethod
    def signin(cls, username, password):
        """Sign in function"""
        user_info = cls.load_user_by_username(username)
        if user_info and cls.check_password(password, user_info["password"]):
            user_instance = cls(username, password)
            for key, value in user_info.items():
                setattr(user_instance, key, value)
            return user_instance
            """
                if key == "id":
                    self.id = value
                elif key == "account_number":
                    self.account_number = value
                elif key == "created_at":
                    self.created_at = value
                elif key == "balance":
                    self.balance = value
                elif key == "first_name":
                    self.first_name = value
                elif key == "last_name":
                    self.last_name = value
                elif key == "email":
                    self.email = value
                elif key == "phone_number":
                    self.phone_number = value
                elif key == "country":
                    self.country = value
                elif key == "city":
                    self.city = value
                elif key == "home_address":
                    self.home_address = value
                elif key == "transaction_history":
                    self.transaction_history = value"""
        else:
            raise AuthenticationError("Invalid username or password!!")

    def create_account(self, **kwargs):
        """Creation of new account for new user."""
        for key, value in kwargs.items():
            if key == "first_name":
                self.first_name = value
            elif key == "last_name":
                self.last_name = value
            elif key == "email":
                self.email = value
            elif key == "phone_number":
                self.phone_number = value
            elif key == "country":
                self.country = value
            elif key == "city":
                self.city = value
            elif key == "home_address":
                self.home_address = value
        if self.first_name and self.last_name and self.email and self.phone_number:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_user()
            print(f"Account created successfully at {self.created_at}!")
        else:
            print("Fill all information required.")

    def authenticate_user():
        while True:
            try:
                username = self.get_valid_username()
                password = self.get_valid_password()
                try:
                    user = self.signin(username, password)
                    return user
                except AuthenticationError as e:
                    print(f"{e} Please try again!")
            except KeyboardInterrupt:
                print("\nThank you for visiting us!")
                print("Exiting............")
                exit()

    def save_user(self):
        """Saving of new user info:
            user = BankEase(username=username, password=password)
        """
        with open("user_data.json", "a") as file:
            user_data = {
                    "id": self.id,
                    "account_number": self.account_number,
                    "created_at": self.created_at,
                    "balance": self.balance,
                    "username": self.username,
                    "password": self.password.decode('utf-8'),
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "phone_number": self.phone_number,
                    "country": self.country,
                    "city": self.city,
                    "home_address": self.home_address,
                    "transaction_history": []
                    }
            json.dump(user_data, file)
            file.write("\n")


class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass


def authenticate_user():
    from models.user import User
    while True:
        try:
            username = User.get_valid_username()
            password = User.get_valid_password()
            try:

                user = User.signin(username, password)
                return user
            except AuthenticationError as e:
                print(f"{e} Please try again!")
        except KeyboardInterrupt:
            print("\nThank you for visiting us!")
            print("Exiting............")
            exit()
