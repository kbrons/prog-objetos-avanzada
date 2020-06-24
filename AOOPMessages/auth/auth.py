from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask import Blueprint
from flask import flash
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from AOOPMessages import db
from AOOPMessages.models import User
from werkzeug.security import check_password_hash, generate_password_hash


auth = Blueprint('auth', __name__)

MAIN_HOME_BLUEPRINT = 'main.home'
AUTH_SIGNUP_BLUEPRINT = 'auth.signup'


@auth.route('/login', methods=['GET'])
def login():
    """This is the Login endpoint.
    Call this endpoint to load the account login form.

    Response codes
    --------
        - 302:
            description: The user is logged in. Redirected to home page.
        - 200:
            description: Returns the Login page with a form to log into an
            account.
    """

    if current_user.is_authenticated:
        return redirect(url_for(MAIN_HOME_BLUEPRINT))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """This is the Login POST endpoint.
    Call this endpoint to log into your account.

    Parameters
    ----------
    email : str
        Email of the user to log into.
    password : str
        Password of the user to log into.

    Response codes
    --------
        - 302:
            - User logged in description: User correctly logged in,
            redirected to Inbox.
            - Bad login data description: Email or password incorrect,
            redirected to Login.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user is not None and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('messages.inbox'))
    else:
        flash('Please check your login details and try again...')
        return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["GET"])
def signup():
    """This is the Sign Up endpoint.
    Call this endpoint to load the account sign up form.

    Response codes
    --------
        - 302:
            description: The user is logged in. Redirected to home page.
        - 200:
            description: Returns the Sign Up page with a form to sign up.
    """

    if current_user.is_authenticated:
        return redirect(url_for(MAIN_HOME_BLUEPRINT))
    return render_template('signup.html')


@auth.route('/signup', methods=["POST"])
def signup_post():
    """This is the Sign Up POST endpoint.
    Call this endpoint to Sign Up an account.

    Parameters
    ----------
    email : str
        Email of the user to log into.
    password : str
        Password of the user to log into.

    Response codes
    --------
        - 302:
            - Sign Up successful description: User correctly signed up
            and logged in, redirected to Inbox.
            - Bad sign up data description: Email or password not present,
            redirected to Sign Up.
            - Email already exists description: Email already belongs to
            a user, redirected to Sign Up.
        - 500:
            description: There was an error creating the user.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        flash('Email is required')
        return redirect(url_for(AUTH_SIGNUP_BLUEPRINT))

    if password is None or password == "":
        flash('Password is required')
        return redirect(url_for(AUTH_SIGNUP_BLUEPRINT))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists...')
        return redirect(url_for(AUTH_SIGNUP_BLUEPRINT))

    new_user = User(email=email,
                    password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for(MAIN_HOME_BLUEPRINT))


@auth.route('/logout')
def logout():
    """This is the Logout endpoint.
    Call this endpoint to log out of your account.

    Response codes
    --------
        - 302:
            description: The user is logged out. Redirected to home page.
    """

    logout_user()
    return redirect(url_for(MAIN_HOME_BLUEPRINT))
