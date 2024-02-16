#!/usr/bin/python3

from models.base import BankEase
from api.v1.app import db


class Transaction(db.Model, BankEase):
    """ A class to handle all transaction of a BankEase system. """
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.BigInteger, db.ForeignKey('accounts.account_number'), nullable=False)
    type = db.Column(db.String(250), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # Define the relationship with the Account model
    # account = db.relationship('Account', backref='transactions')

    def __init__(self, account_number):
        """ Initialisation of Transaction history by Account_number. """
        self.transaction_id = None
        self.account_number = account_number
        self.transaction_type = None
        self.amount = None
        self.balance = None
        self.timestamp = None

    @classmethod
    def create_transaction(cls, account_number, transaction_type, amount, balance):
        """ Transaction history creator for BankEase users. """

        pre_query = '''
        CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        account_number BIGINT NOT NULL,
        type VARCHAR(250) NOT NULL, -- e.g., deposit, withdrawal, transfer
        amount DECIMAL(10, 2) NOT NULL,
        balance DECIMAL(10, 2) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
        '''
        cls.execute_query(pre_query, multi=True)

        query = '''
        INSERT INTO transactions (account_number, type, amount, balance)
        VALUES (%s, %s, %s, %s)
        '''
        values = (account_number, transaction_type, amount, balance)
        cls.execute_query(query, values)

        transaction_instance = cls(account_number)
        transaction_info = get_transaction_by_account_number(account_number)
        if transaction_info:
            transaction_data = transaction_info[0]
            for key, value in transaction_data.items():
                setattr(transaction_instance, key, value)
        else:
            raise Exception("Failed to set transaction atrributes.")

    @classmethod
    def get_transaction_by_account_number(cls, account_number):
        """ Retrieving Transaction info by account_number. """
        query = 'SELECT * FROM transactions WHERE account_number = %s'
        values = (account_number,)
        result = cls.execute_query(query, values)
        return result

    @classmethod
    def set_attribute(cls, transaction_info):
        print("Inside Attribute Function")
        if transaction_info:
            transaction_data = transaction_info[0]
            print(transaction_data)
            account_number = transaction_data["account_number"]
            transaction_instance = cls(account_number)
            for key, value in transaction_data.items():
                setattr(transaction_instance, key, value)
        else:
            raise Exception("Failed to set transaction atrributes.")
