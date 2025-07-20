

#imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#create a form class for adding pantry items
class PantryForm(FlaskForm):
    #ingredient field with a data required validator
    ingredient = StringField('Ingredient: ', validators=[DataRequired()])
    #submit button
    submit = SubmitField('Add Ingredient')