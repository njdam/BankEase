#!/usr/bin/python3
""" Starting Flask Web Application. """

from models.base import BankEase
from models.users import User
from models.accounts import Account
from models.transactions import Transaction
from models.loans import Loan
from flask import Flask, render_template
import uuid


# Flask Application
app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    BankEase.

@app.root('/home', strict_slashes=False)
def BankEase():
    """ BankEase: Modern Online Banking Solution
    Banking Simplified, Anytime, Anywhere
    """
    User.signin()


if __name__ == '__main__':
    "" Running an Api Flask app. """
    app.run(host='0.0.0.0', port=5000, debug=True)
