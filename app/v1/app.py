from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('web/templates/index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    # Add your authentication logic here (check username and password)

    if username == 'example' and password == 'password':
        return 'Login successful!'
    else:
        return 'Login failed. Invalid username or password.'

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Add your authentication logic here (check username and password)

    if username == 'example' and password == 'password':
        return 'Login successful!'
    else:
        return 'Login failed. Invalid username or password.'


if __name__ == '__main__':
    app.run(debug=True)
