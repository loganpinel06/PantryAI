#__init__.py initializes the app package to be used in main.py

#IMPORTS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from google import genai
import os
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#initialize the database
db = SQLAlchemy()

#initialize the login manager for user authentication
login_manager = LoginManager()

#create the Flask application instance
def create_app():
    #create the Flask app
    app = Flask(__name__)

    #configure the apps database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_CONNECTION_STRING')  #PostegreSQL database hosted on Supabase
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #configure the app's secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #initialize the db
    db.init_app(app)

    #initialize the login manager
    login_manager.init_app(app)
    #set the login view for the login manager
    login_manager.login_view = 'auth.login'

    #register the routes blueprint from routes.py
    from .routes import view
    app.register_blueprint(view)

    #register the auth blueprint
    from .auth import view_auth
    app.register_blueprint(view_auth)

    #create the database using a context manager
    with app.app_context():
        db.create_all()

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

