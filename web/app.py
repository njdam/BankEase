#!/usr/bin/python3
""" Starting Flask Web Application. """

import sys
sys.path.append('/home/ubuntu/BankEase')
from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, UserMixin, current_user, logout_user, login_required
from forms import LoginForm
from models.users import User
from api.v1.app import app, login_manager
from werkzeug.security import check_password_hash
from bcrypt import checkpw

@login_manager.user_loader
def load_user(user_id):
    # Load and return the User instance based on the user_id
    try:
        if user_id is not None:
            return User.query.get(int(user_id))
        else:
            return None
    except ValueError:
        return None

app.url_map.strict_slashes = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    # Sigin Page
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return render_template('signin.html', error='Username and password are required')

    user_instance = User.query.filter_by(username=username).first()
    # user_instance = User.signin(username, password)
    # if user_instance and check_password_hash(user_instance.password, password):
    # Entered Password
    encoded_password = password.encode('utf-8')
    # Stored Hashed Password
    stored_password = user_instance.password
    encoded_stored = stored_password.encode('utf-8')

    if user_instance and checkpw(encoded_password, encoded_stored):
        login_user(user_instance)
        return render_template('signin.html', error='Login successful')
        # Redirect to the dashboard for the given user
        account_instance = User.get_account(user_instance)
        # Render the dashboard for the given user with user and account data
        return redirect(url_for('dashboard'))
    else:
        return render_template('signin.html', error='Login failed')
        # Handle invalid login (e.g., show an error message)
        return render_template('signin.html', error='Invalid username or password')

@app.route('/dashboard')
@login_required
def dashboard():
    account_instance = User.get_account(current_user)
    # Render the dashboard for the given user
    return render_template('dashboard.html', User=current_user, Account=account_instance)

@app.route('/profile')
@login_required
def profile():
    account_instance = User.get_account(current_user)
    return render_template('profile.html', User=current_user, Account=account_instance)

@app.route('/logout')
def logout():
    # Logout the user using Flask-Login
    logout_user()
    flash('You have been logged out', 'info')
    # Redirect to the sign-in page after logout
    return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def create_account():
    # Retrieve form data from the request
    username = request.form['username']
    # Check if the username already exists in the database
    if User.username_exists(username):
        error_message = 'Username already taken. Please choose another one.'
        return render_template('signup.html', error=error_message)
    else:
        # Continue processing the rest of the form data
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
        user_created = User.signup(username, password, first_name, last_name, email, phone_number, country, city, home_address, account_type)

        if user_created:
            flash('Account created successfully!', 'success')
        else:
            flash('Failed to create the account. Please try again.', 'error')

        return redirect(url_for('signin'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
