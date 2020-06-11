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


@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('signup.html')


@auth.route('/signup', methods=["POST"])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists...')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.home'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
