#gemini.py will handle the Gemini API interactions

#imports
from google import genai
from google.genai import types
from pydantic import BaseModel
#import the current_app context to access the gemini client from the Flask app
from flask import current_app

#create a pydantic BaseModel for the recipe request
#this will be used to help format Gemini's response to JSON data for easier handling on the frontend
class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]
    instructions: list[str]

#create a method to prompt the Gemini API for a recipe
def generate_recipe(ingredients_list, meal_type):
    """
    Generate recipes using the Gemini API based on provided ingredients and meal type.
    
    Args:
        ingredients_list (list[str]): List of available ingredients
        meal_type (str): Type of meal (e.g., 'breakfast', 'lunch', 'dinner')
    
    Returns:
        Response object from Gemini API containing recipe data, or an error message if error occurs
    """
    #try, except block to handle errors when generating a recipe
    try:
        # Get the gemini_client from the Flask app context
        gemini_client = current_app.gemini_client
        
        #create a prompt for the Gemini API
        prompt = f"Please generate two quality recipes for {meal_type} using the following list of ingredients: {', '.join(ingredients_list)}. Please provide detailed instructions for how to prepare each recipe."

        #send the prompt to the Gemini API
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            #Configure response format to json using the Recipe BaseModel schema and disable thinking
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[Recipe],
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
    #ERROR
    except Exception as e:
        #return the error message (CHANGE THIS FROM PRINT LATER)
        return f"Error generating recipe: {e}"

    #return the response text as JSON data
    return response.text