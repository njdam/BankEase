#!/usr/bin/python3
""" Api Flask Application. """

import sys
# sys.path.append('/home/jeandamn/BankEase/')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import secrets
import os

app = Flask(
    __name__,
    template_folder='/home/ubuntu/BankEase/web/templates',
    static_folder='/home/ubuntu/BankEase/web/static'
)

# Configure the database
# <DB_TYPE>+<DB_CONNECTOR>://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
try:
    # Get environment variables with default values
    db_type = os.environ.get('DB_TYPE', 'mysql')
    db_connector = os.environ.get('DB_CONNECTOR', 'pymysql')
    username = os.environ.get('DB_USERNAME', 'admin')
    password = os.environ.get('DB_PASSWORD', '   ')
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))  # Convert to int with default value
    db_name = os.environ.get('DB_NAME', 'BankEase')

    # Construct the database URL
    DATABASE_URL = f'{db_type}+{db_connector}://{username}:{password}@{host}:{port}/{db_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
except Exception as e:
    print(f'Error retrieving environment variables: {e}')
"""
# Get environment variables
db_type = os.getenv('DB_TYPE')
db_connector = os.getenv('DB_CONNECTOR')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Construct the database URL
DATABASE_URL = f'{db_type}+{db_connector}://{username}:{password}@{host}:{port}/{db_name}'
print(f'DATABASE_URL: {DATABASE_URL}')
# DATABASE_URL = 'mysql+pymysql://admin:"   "@"%":3306/BankEase'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set a secret key for the session
app.config['SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Initialize Flask-Login
login_manager = LoginManager(app)  # login_manager.init_app(app)
login_manager.login_view = 'signin'  # Specify the login view for redirecting unauthenticated users


if __name__ == '__main__':
    app.run(debug=True)
