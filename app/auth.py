

#imports
#import flask
from flask import Blueprint, render_template, session, redirect, url_for
#import Flask-Login
from flask_login import login_user, login_required, logout_user
#impor the RegisterForm and the LoginForm from forms.py
from .forms import RegisterForm
#import the user model from models.py
from .models import User
#import the db object and login manager from __init__.py
from . import db, login_manager

#create a blueprint for the auth routes
view_auth = Blueprint('auth', __name__)

#create a user loader function for Flask-Login
#function allows Flask-Login to know which user is currently logged in
@login_manager.user_loader
def load_user(user_id):
    #query the User model to get the user by id
    return User.query.get(int(user_id))

#create a registration route
@view_auth.route('/register', methods=['GET', 'POST'])
def register():
    #create the registration form
    form = RegisterForm()
    #check if the form is submitted (POST METHOD)
    if form.validate_on_submit():
        #get teh username and password from the form
        username = form.username.data
        password = form.password.data
        #check if the user already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            #if the user already exists, redirect back to the register page with an error message
            return redirect(url_for('auth.register', error='Username already exists'))
        #otherwise, create a new User object
        else:
            #create a new User object
            new_user = User(username=username)
            #set the password hash using the set_password method
            new_user.set_password(password)
            #try, except block to add the new user to the database
            try:
                #connect to the db and add the new user
                db.session.add(new_user)
                #commit the user to the db
                db.session.commit()
                #redirect to the login page after successful registration
                return redirect(url_for('auth.login'))
            #ERROR
            except Exception as e:
                #rollback the user from the db session in case of an error
                db.session.rollback()
                #redirect back to the register page with an error message
                return redirect(url_for('auth.register', error='Error registering user: {}'.format(e)))
    #else we want to render the register template with the form
    return render_template('auth/register.html', form=form)
