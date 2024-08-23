#!/usr/bin/python3
""" Starting Flask Web Application. """

#import sys
#sys.path.append('/home/ubuntu/BankEase')
from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, UserMixin, current_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import Serializer
from forms import LoginForm
from models.users import User
from models.accounts import Account
from models.transactions import Transaction
from api.v1.app import app, login_manager, db
from werkzeug.security import check_password_hash
from bcrypt import checkpw
from werkzeug.utils import secure_filename
from functools import wraps
import os

app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Choose an appropriate folder for uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

# Definition of admin required
def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return view(*args, **kwargs)
        else:
            abort(403)  # Forbidden
    return wrapped_view

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    # Sigin Page
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_instance = User.query.filter_by(username=username, is_admin=False).first()
    if user_instance is None:
        # Handle the case where the user is not found or is not an admin
        flash('Invalid Username or Password!', 'error')
        return redirect(url_for('signin'))

    # Entered Password
    encoded_password = password.encode('utf-8')
    # Stored Hashed Password
    stored_password = user_instance.password
    encoded_stored = stored_password.encode('utf-8')

    if checkpw(encoded_password, encoded_stored):
        login_user(user_instance)
        # Redirect to the dashboard for the given user
        return redirect(url_for('dashboard'))
    else:
        # Handle invalid login (e.g., show an error message)
        flash('Invalid Username or Password!', 'error')

        return redirect(url_for('signin'))

# Sample Flask route for Forgot Password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Check if the email exists in your database
        user = User.query.filter_by(email=email).first()

        if user:
            # If yes, generate a unique token and send a reset email
            token = generate_reset_token(user)
            # Include a link in the email with the token, leading to the password reset page
            send_reset_email(user, token)
            flash('A password reset link has been sent.', 'info')

        else:
            flash('Email not found. Please check your email address and try again.', 'danger')


        return redirect(url_for('login'))

    return render_template('forgot_password.html')

# Sample Flask route for Password Reset
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verify the token and get the associated user
    user = verify_reset_token(token)
    # Check if the token is still valid (not expired)
    if not user:
        flash('Invalid or expired reset token. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        # Update the user's password in the database
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        # Check if the new password and confirm password match
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('reset_password', token=token))

        # Hash the new password
        hashed_password = User.hash_password(new_password)
        # Update the user's password in the database
        user.password = hashed_password
        db.session.commit()
        # Flash a success message
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

# Sample Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'njdamtech@gmail.com'
app.config['MAIL_PASSWORD'] = 'Cr7@DSTVR'
app.config['MAIL_DEFAULT_SENDER'] = 'njdamtech@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Sample Flask route for sending reset email
def send_reset_email(user, token):
    msg = Message('Password Reset Request', sender='njdamtech@gmail.com', recipients=[user.email])
    msg.body = f"Click the following link to reset your password: {url_for('reset_password', token=token, _external=True)}"

    mail.send(msg)

# Token generation logic
def generate_reset_token(user, expiration=3600):
    # Create a serializer with a secret key and an expiration time
    serializer = Serializer(app.config['SECRET_KEY'], expires_in=expiration)

    # Generate a token containing user information
    token = serializer.dumps({'user_id': user.id}).decode('utf-8')

    return token

def verify_reset_token(token):
    # Create a serializer with the secret key
    serializer = Serializer(app.config['SECRET_KEY'])

    try:
        # Deserialize the token to extract the user's id
        data = serializer.loads(token)
        user_id = data['user_id']

        # Retrieve the user object from the database based on the user id
        # Replace 'User' with your actual User model
        user = User.query.get(user_id)

        return user

    except SignatureExpired:
        # Token has expired
        return None
    except BadSignature:
        # Token is invalid
        return None

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
        flash('Username already taken. Please choose another one.', 'error')
        return redirect(url_for('signup'))
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
            return redirect(url_for('signup'))
        else:
            flash('Failed to create the account. Please try again.', 'error')
            return redirect(url_for('signin'))

@app.route('/transaction', methods=['GET'])
@login_required
def transaction():
    user_id = current_user.user_id
    user = current_user
    # Fetch data related to the user by current user_id
    sender_account = Account.query.filter_by(user_id=user_id).first()
    # Fetch transactions from the database, ordered by transaction_id in descending order
    account_number = sender_account.account_number
    transactions = Transaction.query.filter_by(account_number=account_number).order_by(Transaction.transaction_id.desc()).all()
    # Handle GET requests (show the form)
    return render_template('transaction.html', transactions=transactions, account=sender_account, user=user)

@app.route('/loan', methods=['GET'])
@login_required
def loan():
    user_id = current_user.user_id
    # Fetch data related to the user with the provided user_id
    user_instance = User.query.filter_by(user_id=user_id).first()
    # Example: loans = get_loans(user_id)
    loans = User.get_loans(user_instance)
    return render_template('loan.html', loans=loans)

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    user_id = current_user.user_id
    user = current_user
    # Fetch data related to the user by current user_id
    sender_account = Account.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        # Fetch data related to the user with the provided user_id
        recipient = request.form['account_number']
        amount = request.form['amount']

        try:
            # Example: transfers = get_transfers(user_id)
            transfers = sender_account.transfer(recipient, amount)
            flash(transfers, 'success')  # Flash success message
            return redirect(url_for('transfer'))

        except Exception as e:
            flash(f"Transfer failed: {e}", 'error')  # Flash error message
            return redirect(url_for('transfer'))

    # Handle GET requests (show the form)
    return render_template('transfer.html', account=sender_account, user=user)

@app.route('/pay_bill', methods=['GET', 'POST'])
@login_required
def pay_bill():
    user_id = current_user.user_id
    user = current_user
    # Fetch data related to the user by current user_id
    sender_account = Account.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        # Fetch data related to the user with the provided user_id
        account_number = request.form['bill_account']  # Bill account_number
        amount = request.form['amount']
        try:
            # Example: bills = get_bills(user_id)
            bills = sender_account.transfer(account_number, amount)
            flash(bills, 'success')
            return redirect(url_for('pay_bill'))

        except Exception as e:
            flash(f"Payment failed: {e}", 'error')  # Flash error message
            return redirect(url_for('pay_bill'))

    # Handle GET requests (show the form)
    return render_template('pay_bill.html', account=sender_account, user=user)

# Admin Authenticating and their functionality
@app.route('/signin/admin')
def signin_admin():
    return render_template('signin_admin.html')

@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user_instance = User.query.filter_by(username=username, is_admin=True).first()
    if user_instance is None:
        # Handle the case where the user is not found or is not an admin
        flash('User is not found or is not an admin!', 'error')
        return redirect(url_for('signin_admin'))

    # Entered Password
    encoded_password = password.encode('utf-8')
    # Stored Hashed Password
    stored_password = user_instance.password
    encoded_stored = stored_password.encode('utf-8')

    if checkpw(encoded_password, encoded_stored):
        login_user(user_instance)
        # Redirect to the dashboard for the given admin user
        return redirect(url_for('admin_dashboard'))
    else:
        # Handle invalid login (e.g., show an error message)
        flash('Invalid Username or Password!', 'error')
        return redirect(url_for('signin_admin'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Admin dashboard logic
    if current_user.is_admin:
        account_instance = User.get_account(current_user)
        return render_template('admin_dashboard.html', User=current_user, Account=account_instance)
    else:
        abort(403)  # Forbidden

@app.route('/admin/profile')
@login_required
def admin_profile():
    if current_user.is_admin:
        # Fetch admin profile information
        return render_template('admin_profile.html', User=current_user)
    else:
        abort(403)  # Forbidden

@app.route('/admin/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.is_admin:
        if request.method == 'POST':
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
            is_admin_str = request.form['isAdmin']
            # Convert to boolean (default to False if not provided or not recognized)
            is_admin = is_admin_str.lower() == 'true' if is_admin_str else False
            try:
                # Create a new user
                user_created = User.create_user(
                        username, password, first_name, last_name, email,
                        phone_number, country, city, home_address,
                        account_type, is_admin)

                flash('User created successfully!', 'success')
                return redirect(url_for('user_list'))

            except Exception as e:
                flash(f'Failed to create the user due to {e}. Please try again.', 'error')
                return redirect(url_for('create_user'))

        return render_template('create_user.html')

    else:
        abort(403)  # Forbidden

@app.route('/user_list')
@login_required
def user_list():
    if current_user.is_admin:
        # Retrieve all users from the database
        users = User.query.all()
        return render_template('user_list.html', users=users)
    else:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    # Retrieve the user from the database
    user = User.query.get_or_404(user_id)

    try:
        # Delete the user and associated accounts
        User.delete_user(user_id)
        flash('User and associated accounts deleted successfully!', 'success')
    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        flash(f'Failed to delete user and accounts: {e}', 'error')

    return redirect(url_for('user_list'))


@app.route('/get_recipient_details', methods=['POST'])
def get_recipient_details():
    account_number = request.form.get('account_number')
    print(f"Received request for account number: {account_number}")
    # Query the database to get recipient details
    #recipient_account = Account.query.filter_by(account_number=account_number).first()

    # Fetch the associated user by db relationship named 'user'
    '''if recipient_account:
        user = recipient_account.user'''
    user = User.query.join(Account).filter(Account.account_number == account_number).first()
    if user:
        # Assuming you have a username attribute in your User model
        full_name = f"{user.first_name} {user.last_name}"
        return jsonify({'full_name': full_name})
    else:
        return jsonify({'error': 'Account not found'})

@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profilePicture' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['profilePicture']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Securely save the file with the desired filename
        filename = secure_filename(f"{User.username}_profile.png")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Profile picture uploaded successfully', 'success')
    else:
        flash('Invalid file type. Allowed types are png, jpg, jpeg, gif', 'error')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/deposit/<int:user_id>', methods=['POST'])
@login_required
def admin_deposit(user_id):
    # Logic to deposit money to the account of the specified user
    pass

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    # Logic to delete the specified user
    pass

@app.route('/admin/loan/<int:user_id>', methods=['POST'])
@login_required
def admin_loan_user(user_id):
    # Logic to lend loan to the specified user
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    flash('Sorry for Inconvenience. Please try again later! Is under development.', 'error')
    return redirect(url_for('signin_admin'))
    #return render_template('500.html'), 500

@app.errorhandler(502)
def bad_request_error():
    return render_template('502.html'), 502


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
