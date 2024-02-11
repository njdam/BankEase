#!/usr/bin/python3
""" Starting Flask Web Application. """

from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from ..models.users import User
from ..models.accounts import Account

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/signin')
def signin():
    return render_template('templates/signin.html')

@app.route('/login', methods=['POST'])
def login():
    # Retrieve form data from request
    username = request.form['username']
    password = request.form['password']
    User.signin()

@app.route('/logout')
def logout():
    # Implement logic for logout
    return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('templates/signup.html')

@app.route('/register', methods=['POST'])
def create_account():
    # Retrieve form data from the request
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    phone_number = request.form['phoneNumber']
    country = request.form['country']
    city = request.form['city']
    home_address = request.form['homeAddress']
    account_type = request.form['accountType']

    # Process the data (for simplicity, just printing here)
    User.create_user(username, password, first_name, last_name, email, phone_number, country, city, home_address)
    Account.create_account(User.user_id, account_type)
    print(f"Username: {username}")
    print(f"Password: {password}")
    # ... (print other form data)

    # In a real-world application, you would store the data in a database

    return "Account created successfully!"

if __name__ == '__main__':
    app.run(debug=True)