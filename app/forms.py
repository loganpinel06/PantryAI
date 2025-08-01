

#imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo

#create a form class for the RegisterForm
class RegisterForm(FlaskForm):
    #create the fields
    #see message parameter in validators to see what is required for username and password
    username = StringField('Username: ', validators=[DataRequired(), Length(min=6, max=30, message='Username must be between 6 and 30 characters long'), 
                                                     Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', message='Username must contain upper and lower case letters, and at least one number')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long'), 
                                                       Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).+$', message='Password must contain upper and lower case letters, at least one number, and one special character')])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

#create a form class for the LoginForm
class LoginForm(FlaskForm):
    #create the fields
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

#create a form class for adding pantry items
class PantryForm(FlaskForm):
    #ingredient field with a data required validator
    ingredient = StringField('Ingredient: ', id='ingredient-input', validators=[DataRequired()])
    #submit button
    submit = SubmitField('Add Ingredient', id='submit-button')

#create a form class for generating recipes
class GenerateRecipesForm(FlaskForm):
    #users need to select a meal type before generating recipes
    #meal_type field with a radio button for breakfast, lunch, or dinner
    #note: choices are touples, 'breakfast' is whats sent to the server, 'Breakfast' is what is displayed to the page
    meal_type = RadioField('Meal Type: ', choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], 
                            validators=[DataRequired()], default='breakfast')
    #submit button
    submit = SubmitField('Generate Recipes', id='meal-type-submit')