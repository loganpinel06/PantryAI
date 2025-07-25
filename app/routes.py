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
    
#create the main route to view all pantry items and render the pantry.html template
@view.route('/pantry', methods=['GET'])
def pantry():
    #creat the PantryForm instance
    pantry_form = PantryForm()
    #query the Pantry model to get all pantry items
    pantry_items = Pantry.query.all()
    #render the pantry.html template with the pantry items
    return render_template('pantry.html', pantry_items=pantry_items, form=pantry_form)

#create an api route to add (POST) a new pantry item
#functionality for the DOM will be implemented in the pantry.js file
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
            #rollback the Pantry object from the db session in case of an error
            db.session.rollback()
            #return the error message
            return jsonify({
                'error': 'Error adding pantry item: {}'.format(e)
            }), 500 # HTTP status code 500 for server error
    #else return a json response with the form errors
    else:
        return jsonify({
            'errors': pantry_form.errors
        })
    
#create an api route to delete a pantry item from the database
#functionality for the DOM will be implemented in the pantry.js file
@view.route('/api/pantry/delete-ingredient/<int:id>', methods=['DELETE'])
def delete_ingredient(id:int):
    #query the Pantry model to get the pantry item by id
    pantry_item_to_delete = Pantry.query.get_or_404(id)
    #try, except block to delete the pantry item from the database and handle errors
    try:
        #connect to the db and delete the pantry item
        db.session.delete(pantry_item_to_delete)
        #commit the transaction to the db
        db.session.commit()
        #return a json response with a success message
        return jsonify({
            'id': pantry_item_to_delete.id,
            'ingredient': pantry_item_to_delete.ingredient
        }), 200 # HTTP status code 200 for success
    #ERROR
    except Exception as e:
        #return the error message
        return jsonify({
            'error': 'Error deleting pantry item: {}'.format(e)
        }), 500 # HTTP status code 500 for server error