#__init__.py initializes the app package to be used in main.py

#IMPORTS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from google import genai
import os
from dotenv import load_dotenv
#import datetime for session lifetime management
from datetime import timedelta

#load environment variables
load_dotenv()

#initialize the database
db = SQLAlchemy()

#initialize the login manager for user authentication
login_manager = LoginManager()

#setup the rate limiter for the app
#use deferred initialization so we can keep app modular
#limiter will be used in auth.py
limiter = Limiter(key_func=get_remote_address,
                  storage_uri=os.getenv('REDIS_URI')) #connect to Upstash Redis to store rate limiting data in-memory

#create the Flask application instance
def create_app():
    #create the Flask app
    app = Flask(__name__)

    #configure the apps database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_CONNECTION_STRING')  #PostegreSQL database hosted on Supabase
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #add session and cookie security
    app.config['SESSION_COOKIE_SECURE'] = True #Ensure cookies are only sent over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True #Prevent XSS attacks by making cookies inaccessible to JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' #Help prevent CSRF attacks

    #configure a Session Lifetime
    #sessions will expire after 30 minutes of inactivity
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    #configure the app's secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #initialize the db
    db.init_app(app)

    #initialize the login manager
    login_manager.init_app(app)
    #set the login view for the login manager
    login_manager.login_view = 'auth.login'

    #initialize the rate limiter
    limiter.init_app(app)

    #register the routes blueprint from routes.py
    from .routes import view
    app.register_blueprint(view)

    #register the auth blueprint
    from .auth import view_auth
    app.register_blueprint(view_auth)

    #create the database using a context manager
    with app.app_context():
        #check if we are in production or development
        #if development, we wil create the database, otherwise there is no need since it already exists in production
        #THIS WAS ADDED TO SAVE TIME FOR RENDER BOOTUPS
        if os.getenv('FLASK_ENV') == 'development':
            #create the database
            db.create_all()
        #else we can just pass
        else:
            pass

    #initialize the Gemini client
    #get the api key from the .env file
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    #make sure the api key exists
    if gemini_api_key:
        #setup the gemini client with the api key and store it in the app context
        app.gemini_client = genai.Client(api_key=gemini_api_key)
    #incase of errors, print an error message (CHANGE THIS FROM PRINT LATER)
    else:
        print("Warning: GENAI_API_KEY not found in environment variables")
        app.gemini_client = None

    #return the app instance
    return app

