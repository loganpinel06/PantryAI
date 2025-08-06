#

#imports
from flask import Blueprint, render_template, redirect, url_for, jsonify, request
#import the Flask-Login for user authentication
from flask_login import login_required, current_user
#import the Pantry and SavedRecipes models
from .models import Pantry, SavedRecipes
#import the generate_recipe function from the gemini client
from .gemini import generate_recipe
#import the db object from __init__.py to connect to the database
from . import db
#import the Flask-WTF forms from forms.py
from .forms import PantryForm, GenerateRecipesForm
#import json module to handle JSON parsing
import json

#create a blueprint for the routes
view = Blueprint('view', __name__)

###########
#MAIN ROUTES WHICH RENDER HTML TEMPLATES
#these routes will handle the main views of the application
###########
#create the main route to view all pantry items and render the pantry.html template
@view.route('/pantry', methods=['GET'])
@login_required  #require user to be logged in to access this route
def pantry():
    #create the PantryForm and GenerateRecipesForm instance
    pantry_form = PantryForm()
    recipe_form = GenerateRecipesForm()
    #query the Pantry model to get all pantry items for the current user
    pantry_items = Pantry.query.filter_by(user_id=current_user.id).all()
    #render the pantry.html template with the pantry items
    return render_template('pantry.html', pantry_items=pantry_items, pantry_form=pantry_form, recipe_form=recipe_form)

###########
#API ROUTES
#these routes will handle the API requests for the pantry items and recipes
###########
#create an api route to add (POST) a new pantry item
#functionality for the DOM will be implemented in the pantry.js file
@view.route('/api/pantry/add-ingredient', methods=['POST'])
@login_required  #require user to be logged in to access this route
def add_ingredient():
    #create the PantryForm instance
    pantry_form = PantryForm()
    #check if the form is submitted (POST METHOD)
    if pantry_form.validate_on_submit():
        #get the data from the form
        ingredient = pantry_form.ingredient.data
        #create a new Pantry object with the current user's id
        new_pantry_object = Pantry(ingredient=ingredient, user_id=current_user.id)
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
@login_required  #require user to be logged in to access this route
def delete_ingredient(id:int):
    #query the Pantry model to get the pantry item by id and ensure it belongs to the current user
    pantry_item_to_delete = Pantry.query.filter_by(id=id, user_id=current_user.id).first_or_404()
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
    
#HANDLE THE API ROUTES FOR USING GEMINI API
@view.route('/api/gemini/generate-recipes', methods=['POST'])
@login_required  #require user to be logged in to access this route
def generate_recipes():
    #query the Pantry model to get all pantry items for the current user
    pantry_items = Pantry.query.filter_by(user_id=current_user.id).all()
    #create an instance of the GenerateRecipesForm
    recipe_form = GenerateRecipesForm()
    #check if the form is submitted (POST METHOD)
    if recipe_form.validate_on_submit():
        #try, except block to handle errors when generating recipes
        try:
            #get the meal type from the form
            meal_type = recipe_form.meal_type.data
            #create a list of ingredients from the pantry items using list comprehension
            ingredients_list = [item.ingredient for item in pantry_items]
            #call the generate_recipe function from the gemini client
            #pass the ingredients_list and meal_type to the function
            response = generate_recipe(ingredients_list, meal_type)
            #parse the JSON response from Gemini and return it as proper JSON
            recipes_data = json.loads(response)
            return jsonify(recipes_data)
        #ERROR
        except Exception as e:
            #return the error message
            return jsonify({
                'error': 'Error generating recipes: {}'.format(e)
            }), 500
        
#create an api route to save a recipe to the user's saved recipes
@view.route('/api/gemini/save-recipe', methods=['POST'])
@login_required  #require user to be logged in to access this route
def save_recipe():
    #get the recipe data from the request JSON
    recipe_data = request.json
    #check if the recipe already exists for the user
    existing_recipe = SavedRecipes.query.filter_by(
        user_id=current_user.id,
        recipe={
            'recipe_name': recipe_data['recipe'],
            'ingredients': recipe_data['ingredients'],
            'instructions': recipe_data['instructions']
        },
        meal_type=recipe_data['meal_type']
    ).first()
    #if the recipe already exists, return an error message
    if existing_recipe:
        return jsonify({
            'error': 'Recipe already saved.'
        }), 400  # HTTP status code 400 for bad request
    #else, create a new SavedRecipes object
    else:
        #create a new SavedRecipes object with the current user's id
        #store the entire recipe data as JSON (recipe name, ingredients, instructions)
        new_saved_recipe = SavedRecipes(
            user_id=current_user.id,
            recipe={
                'recipe_name': recipe_data['recipe'],
                'ingredients': recipe_data['ingredients'],
                'instructions': recipe_data['instructions']
            },
            meal_type=recipe_data['meal_type']
        )
        #try, except block to handle errors when saving the recipe
        try:
            #connect to the db and add the saved recipe object
            db.session.add(new_saved_recipe)
            #commit the SavedRecipes object to the db
            db.session.commit()
            #return a json response with the saved recipe data
            return jsonify({
                'message': 'Recipe saved successfully',
            }), 200  # HTTP status code 200 for success
        #ERROR
        except Exception as e:
            #rollback the SavedRecipes object from the db session in case of an error
            db.session.rollback()
            #return the error message
            return jsonify({
                'error': 'Error saving recipe: {}'.format(e)
            }), 500