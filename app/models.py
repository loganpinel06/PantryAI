#imports
from . import db
#import flask_login for user authentication
from flask_login import UserMixin
#import wekzeug.security for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
#import JSONB for handling JSON data specifically with PostgreSQL
from sqlalchemy.dialects.postgresql import JSONB

#create the User model to store user information
class User(UserMixin, db.Model):
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #username field
    username = db.Column(db.String(50), unique=True, nullable=False)
    #password field
    password = db.Column(db.String(300), nullable=False)
    #define a relationship with the Pantry model and the SavedRecipes model
    #this will allow us to access the user's pantry items and saved recipes
    pantry_items = db.relationship('Pantry', backref='user', lazy=True)
    saved_recipes = db.relationship('SavedRecipes', backref='user', lazy=True)

    #override the __repr__ method to return a string represenation of the Users object's id
    def __repr__(self):
        return "User {}".format(self.id)
    
    #create a method to set the password hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    #create a method to check the password hash
    def check_password(self, password):
        return check_password_hash(self.password, password)

#create the Pantry model
class Pantry(db.Model):
    #create a user_id foreign key to link a pantry object to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #ingredient field
    ingredient = db.Column(db.String(50), nullable=False)

    #override the __repr__ method to return a string representation of the Pantry object's id
    def __repr__(self):
        return "Pantry {}".format(self.id)
    
#create the SavedRecipes model to store saved recipes
class SavedRecipes(db.Model):
    #create a user_id foreign key to link a pantry object to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #recipe field
    recipe = db.Column(JSONB, nullable=False)
    #meal_type field
    meal_type = db.Column(db.String(10), nullable=False)
    #create a recipe_name field for easily checking if a recipe already exists
    recipe_name = db.Column(db.String(100), nullable=False)

    #override the __repr__ method to return a string representation of the SavedRecipes object's id
    def __repr__(self):
        return "SavedRecipes {}".format(self.id)