from database import get_user
from crypto import generate_token, verify_and_decrypt_token
from flask import Flask, make_response, render_template, request, redirect, url_for, session, flash
import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../shared')))

app = Flask(__name__)
# Session key used to encrypt the session data (done by Flask)
app.secret_key = 'super-secret-key-service2'

SERVICE_HEADER = b"Service 2"


def check_token():
    token = request.cookies.get('auth_token')
    if token:
        try:
            message = verify_and_decrypt_token(token)
            session['username'] = message['username']
        except ValueError:
            session.pop('username', None)


@app.route('/')
def home():
    check_token()

    if 'username' in session:
        return render_template('home.html', title='Home', username=session['username'])
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    check_token()

    # Check if the user is alredy logged in
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)
        if user and user[1] == password:
            # Generate token and set in cookie
            token = generate_token(username, SERVICE_HEADER)
            response = make_response(redirect(url_for('home')))

            # Argument max_age is left empy to make the cookie a session cookie
            response.set_cookie('auth_token', token)

            # Save the username in the session. This is used for this service locally and has nothing to do with the SSO functionality
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return response
        else:
            flash('Incorrect username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)

    response = make_response(redirect(url_for('home')))

    # Delete the cookie responsible for SSO
    response.set_cookie('auth_token', '', expires=0)

    flash('Logged out successfully!', 'success')
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5001)
