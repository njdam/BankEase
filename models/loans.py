#!/usr/bin/python3

from models.base import BankEase
from api.v1.app import db


class Loan(db.Model, BankEase):
    """ A class to handle loan on BankEase System. """
    __tablename__ = 'loans'

    loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    interest_rate = db.Column(db.DECIMAL(5, 2), nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define the relationship with the User model
    #user = db.relationship('User', backref='loans')

    def __init__(self, user_id):
        """Initialisation of Loan info by user_id. """
        self.loan_id = None
        self.user_id = user_id
        self.amount = None
        self.interest_rate = None
        self.term_months = None
        self.status = None
        self.created_at = None

    @classmethod
    def create_loan(cls, user_id, amount, interest_rate, term_months, status):
        """ Loan Initialisation Class. """

        pre_query = '''
        CREATE TABLE IF NOT EXISTS loans (
        loan_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        interest_rate DECIMAL(5, 2) NOT NULL,
        term_months INT NOT NULL,
        status VARCHAR(50) NOT NULL, -- e.g., pending, approved, rejected
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        '''
        cls.execute_query(pre_query)

        query = '''
        INSERT INTO loans (user_id, amount, interest_rate, term_months, status)
        VALUES (%s, %s, %s, %s, %s)
        '''
        values = (user_id, amount, interest_rate, term_months, status)
        cls.execute_query(query, values)

        loan_instance = cls(user_id)
        loan_info = get_loan_by_user_id(user_id)
        if loan_info:
            loan_data = transaction_info[0]
            for key, value in loan_data.items():
                setattr(loan_instance, key, value)
        else:
            raise Exception("Failed to set Loan atrributes.")

    @classmethod
    def get_loan_by_user_id(user_id):
        """ Retrieving loan information by user_id. """
        query = 'SELECT * FROM loans WHERE user_id = %s'
        values = (user_id,)
        result = cls.execute_query(query, values)
        return result
