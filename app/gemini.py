#gemini.py will handle the Gemini API interactions

#imports
from google import genai
from . import genai_client

#create a method to prompt the Gemini API for a recipe
def generate_recipe(ingredients_list, meal_type):
    #create a prompt for the Gemini API
    prompt = f"Please generate two quality recipes for {meal_type} using the following list of ingredients: {', '.join(ingredients_list)}"

    #send the prompt to the Gemini API
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
        #Disable thinking (CODE FROM GEMINI API DOCS)
        #this will reduce the response time and token usage/costs
        config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )

    #return the response text
    return response
