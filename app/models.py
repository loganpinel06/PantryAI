#imports
from . import db

#create the Pantry model
class Pantry(db.Model):
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #ingredient field
    ingredient = db.Column(db.String(50), nullable=False)

    #override the __repr__ method to return a string representation of the Pantry object's id
    def __repr__(self):
        return "Pantry {}".format(self.id)
