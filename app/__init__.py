# app package initialization
from flask import Flask

#create the Flask application instance
def create_app():
    #create the Flask app
    app = Flask(__name__)

    #return the app instance
    return app

