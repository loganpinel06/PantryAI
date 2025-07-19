#__init__.py initializes the app package to be used in main.py

#IMPORTS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialize the database
db = SQLAlchemy()

#create the Flask application instance
def create_app():
    #create the Flask app
    app = Flask(__name__)

    #configure the apps database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #initialize the db
    db.init_app(app)

    #create the database using a context manager
    with app.app_context():
        db.create_all()

    #return the app instance
    return app

