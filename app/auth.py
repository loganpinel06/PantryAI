

#imports
#import flask
from flask import Blueprint, render_template, session, redirect, url_for
#import Flask-Login
from flask_login import login_user, login_required, logout_user
#import the user model from models.py
from .models import User
#import the db object and login manager from __init__.py
from . import db, login_manager

#create a blueprint for the auth routes
view_auth = Blueprint('auth', __name__)
