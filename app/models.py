#imports
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#create the User model to store user information
class User(UserMixin, db.Model):
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #username field
    username = db.Column(db.String(50), unique=True, nullable=False)
    #password field
    password = db.Column(db.String(300), nullable=False)
    #define a relationship with the Pantry model
    pantry_items = db.relationship('Pantry', backref='user', lazy=True)

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
