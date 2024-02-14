#!/usr/bin/python3
""" Starting Flask Web Application. """

import sys
sys.path.append('/home/jeandamn/BankEase')
from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, UserMixin, current_user
from auth import login_manager
import secrets
from models.users import User

app = Flask(__name__)
# Set a secret key for the session
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configure the database
DATABASE_URL = 'mysql+pymysql://admin:"   "@localhost:3306/BankEase'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load and return the User instance based on the user_id
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login', methods=['POST'])
def login():
    # Retrieve form data from request
    username = request.form['username']
    password = request.form['password']
    user_instance = User.signin(username, password)
    if user_instance:
        login_user(user_instance)
        # Redirect to the dashboard for the given user
        account_instance = User.get_account(user_instance)
        # Render the dashboard for the given user with user and account data
        return render_template('dashboard.html', User=user_instance, Account=account_instance)
    else:
        # Handle invalid login (e.g., show an error message)
        return render_template('signin.html', error='Invalid username or password')

@app.route('/<username>')
def dashboard(username):
    user_instance = current_user
    account_instance = User.get_account(user_instance)
    # Render the dashboard for the given user
    return render_template('dashboard.html', User=user_instance, Account=account_instance)

@app.route('/logout')
def logout():
    # Implement logic for logout
    return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

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
    User.signup(username, password, first_name, last_name, email, phone_number, country, city, home_address, account_type)
    return redirect(url_for('signin'))

    # In a real-world application, you would store the data in a database
    return "Account created successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
