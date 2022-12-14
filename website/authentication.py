from flask import Blueprint, render_template, request, flash, redirect, url_for
from .DBmodel import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    """Function to log in the user. """
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('This email does not exist.', category='error')


    return render_template("login.html", user=current_user)
    


@auth.route('/logout')
@login_required
def logout():

    """Log out the user."""

    flash('Logged out successfully!', category='success')
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    """
    
    Sign up the user. Query the information from the form, and add them to the Database, if all requirements are met. 
    
    """

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Try logging in.', category='error')
        elif len(email) < 4:
            flash('Email is too short. Email must be contain more than 3 characters.', category='error')
        elif len(first_name) < 3:
            flash('First name must contain more than 2 characters.', category='error')
        elif len(last_name) < 3:
            flash('Last name must contain more than 2 characters.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name = last_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

    
