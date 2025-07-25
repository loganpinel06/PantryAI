#__init__.py initializes the app package to be used in main.py

#IMPORTS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#initialize the database
db = SQLAlchemy()

#initialize the login manager for user authentication
login_manager = LoginManager()

#create the Flask application instance
def create_app():
    #create the Flask app
    app = Flask(__name__)

    #configure the apps database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'  # SQLite database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #configure the app's secret key for session management
    app.config['SECRET_KEY'] = 'secret_key'

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

    #return the app instance
    return app

