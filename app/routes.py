#

#imports
from flask import Blueprint, render_template, url_for
#import the Pantry model
from .models import Pantry
#import the db object from __init__.py to connect to the database
from . import db

#create a blueprint for the routes
view = Blueprint('view', __name__)

#create a test route
@view.route('/', methods=['GET'])
def index():
    #query the database for all pantry items
    pantry_items = Pantry.query.all()
    #render the index template with the pantry items
    return render_template('index.html', pantry_items=pantry_items)