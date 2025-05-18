from . import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash

from .models import User
from .forms import LoginForm, RegisterForm


authbp = Blueprint('auth', __name__)


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==username))
        if user is None:
            error = 'Username or password is incorrect.'
            print('INFO: Username or password is incorrect.')
        elif not check_password_hash(user.password_hash, password):
            error = 'Username or password is incorrect.'
            print('INFO: Username or password is incorrect.')
        if error is None:
            login_user(user)
            print('INFO: Successfully logged in')
            flash('You have logged in successfully')
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    # Ensure that the validate_on_submit returns true
    if register_form.validate_on_submit():
        # Fetch the data from the register form
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        # Check if a user with the username already exists
        user = db.session.scalar(db.select(User).where(User.name==username))
        if user:
            flash('Username is already taken, please try another.')
            print('INFO: Username already exists in database.')
            return redirect(url_for('auth.register'))
        # Hash the password for DB storage
        password_hash = generate_password_hash(password)
        # Create a new user to store in the DB
        new_user = User(name = username, password_hash = password_hash, email_id = email)
        db.session.add(new_user)
        db.session.commit()
        # Print message to console and redirect the user to the login page
        print('INFO: Successfully registered a new user.')
        flash('You have successfully created an account and can now login.')
        return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register_form, heading='Register')


@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    print('INFO: Successfully logged out a user.')
    return redirect(url_for('main.index'))
