#!/usr/bin/python3

from models.base import BankEase
from models.transactions import Transaction
from api.v1.app import db
from decimal import Decimal


class Account(db.Model, BankEase):
    """ A class to create BankEase account information by user. """
    __tablename__ = 'accounts'

    account_number = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define the relationship with the User model
    #user = db.relationship('User', backref='accounts')
    transactions = db.relationship('Transaction', backref='accounts')

    def __init__(self, user_id):
        """ Initialisation of Account information for the User. """
        self.account_number = None
        self.user_id = user_id
        self.account_type = None
        self.balance = 0

    @classmethod
    def create_account(cls, user_id, account_type, balance=0.0):
        """ A function to create a BankEase account in mysql database
        accounts table corresponding to user_id of a User.
        """
        pre_query = '''
        CREATE TABLE IF NOT EXISTS accounts (
        account_number BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        account_type VARCHAR(50) NOT NULL, -- e.g., savings, checking
        balance DECIMAL(10, 2) DEFAULT 0.00,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ) AUTO_INCREMENT = 970321240000; -- Set the initial value to startOn        '''
        cls.execute_query(pre_query, multi=True)

        query = '''
        INSERT INTO accounts (user_id, account_type, balance)
        VALUES (%s, %s, %s)
        '''
        values = (user_id, account_type, balance)
        cls.execute_query(query, values)

        account_instance = cls(user_id)
        account_info = cls.get_account_by_user_id(user_id)
        if account_info:
            account_data = account_info[0]
            for key, value in account_data.items():
                setattr(account_instance, key, value)
        else:
            raise Exception("Failed to set Account atrributes.")

    @classmethod
    def get_account_by_user_id(cls, user_id):
        """ Retrieving Account info by user_id. """
        query = 'SELECT * FROM accounts WHERE user_id = %s'
        values = (user_id,)
        result = cls.execute_query(query, values)
        return result

    @classmethod
    def get_account_by_account_number(cls, account_number):
        """ Retrieving Account info by account_number. """
        query = 'SELECT * FROM accounts WHERE account_number = %s'
        values = (account_number,)
        result = cls.execute_query(query, values)
        if result:
            account_data = result[0]
            account_instance = cls(account_data['user_id'])
            for key, value in account_data.items():
                setattr(account_instance, key, value)
            return account_instance
        else:
            raise Exception("Account number doesn't exists!")

    def get_transactions(self):
        """ Retrieving Transaction info by account_number. """
        query = 'SELECT * FROM transactions WHERE account_number = %s'
        values = (self.account_number,)
        transactions = self.execute_query(query, values)
        if transactions:
            return transactions
        else:
            return None
            # raise Exception("No transactions!")

    def update_balance(self):
        """ Update the balance in the database. """
        query = 'UPDATE accounts SET balance = %s WHERE account_number = %s'
        values = (self.balance, self.account_number)
        self.execute_query(query, values)

    def deposit(self, amount):
        """A function to deposit amount of money."""
        transaction_type = 'deposit'

        try:
            amount = float(amount)
            self.balance = float(self.balance)
            self.balance += amount
            self.update_balance() # Updating Balance in DataBase
            # Update transaction history
            query = '''
            INSERT INTO transactions (account_number, type, amount, balance)
            VALUES (%s, %s, %s, %s)
            '''
            values = (self.account_number, transaction_type, amount, self.balance)
            self.execute_query(query, values)
            # save updated user information
            deposits = f"Deposited ${amount} at {self.account_number}.\nCurrent Balance: ${self.balance}"

        except Exception as e:
            deposits = f"Failed to deposit: {e}"

        return (deposits)

    def withdraw(self, amount):
        """A function to withdraw amount of money."""
        transaction_type = 'withdraw'

        try:
            amount = float(amount)
            self.balance = float(self.balance)
            if self.balance > amount:
                self.balance -= amount
                self.update_balance() # Updating Balance in DataBase
                # Update transaction history
                query = '''
                INSERT INTO transactions (
                account_number, type, amount, balance)
                VALUES (%s, %s, %s, %s)
                '''
                values = (
                        self.account_number, transaction_type,
                        amount, self.balance
                        )
                self.execute_query(query, values)
                withdrawns = f"Withdrawn ${amount} at {self.account_number}.\nCurrent Balance: ${self.balance}"
            else:
                withdrawns = "Insuficient Funds!"

            return (withdrawns)

        except Exception as e:
            withdrawns = f"Failed to withdraw: {e}"

        return (withdrawns)

    def transfer(self, account_number, amount):
        """A function to transfer amount of money to another user."""
        transaction_type = 'transfer'

        try:
            recipient = self.get_account_by_account_number(account_number)
            amount = Decimal(amount)
            self.balance = Decimal(self.balance)
            recipient.balance = Decimal(recipient.balance)
            if self.balance >= amount > 0:
                self.balance -= amount
                recipient.balance += amount
                # Updating Balance of sender in DataBase
                self.update_balance()
                # Updating Balance of receiver in DataBase
                recipient.update_balance()

                # Updating transaction history sender
                query = '''
                INSERT INTO transactions (
                account_number, type, amount, balance)
                VALUES (%s, %s, %s, %s)
                '''
                values = (
                        self.account_number, transaction_type,
                        amount, self.balance
                        )
                self.execute_query(query, values)

                # Updating transaction history of receiver
                transaction_type = "Received"
                query = '''
                INSERT INTO transactions (
                account_number, type, amount, balance)
                VALUES (%s, %s, %s, %s)
                '''
                values = (
                        recipient.account_number, transaction_type,
                        amount, recipient.balance
                        )
                self.execute_query(query, values)
                transfers = f"{self.account_number}(You) Transferred ${amount} to {recipient.account_number}.\nCurrent Balance: ${self.balance}"

            else:
                transfers = "Insuficient Funds!"
            
            return (transfers)

        except Exception as e:
            transfers = f"Failed to Transfer: {e}"

        return (transfers)
