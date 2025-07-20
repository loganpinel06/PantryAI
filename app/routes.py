#

#imports
from flask import Blueprint, render_template, redirect, url_for, jsonify
#import the Pantry model
from .models import Pantry
#import the db object from __init__.py to connect to the database
from . import db
#import the Flask-WTF forms from forms.py
from .forms import PantryForm

#create a blueprint for the routes
view = Blueprint('view', __name__)
    
#create the main route to view all pantry items
@view.route('/', methods=['GET'])
def index():
    #creat the PantryForm instance
    pantry_form = PantryForm()
    #query the Pantry model to get all pantry items
    pantry_items = Pantry.query.all()
    #render the pantry.html template with the pantry items
    return render_template('pantry.html', pantry_items=pantry_items, form=pantry_form)

#create an api route to add (POST) a new pantry item
@view.route('/api/pantry/add-ingredient', methods=['POST'])
def add_ingredient():
    #create the PantryForm instance
    pantry_form = PantryForm()
    #check if the form is submitted (POST METHOD)
    if pantry_form.validate_on_submit():
        #get the data from the form
        ingredient = pantry_form.ingredient.data
        #create a new Pantry object
        new_pantry_object = Pantry(ingredient=ingredient)
        #try, except block to add the Pantry object to the database
        try: 
            #connect to the db and add the pantry object
            db.session.add(new_pantry_object)
            #commit the transaction to the db
            db.session.commit()
            #return a json response with the new pantry item
            return jsonify({
                'id': new_pantry_object.id,
                'ingredient': new_pantry_object.ingredient
            })
        #ERROR
        except Exception as e:
            #return the error message
            return 'Error: {}'.format(e)
    #else return a json response with the form errors
    else:
        return jsonify({
            'errors': pantry_form.errors
        })