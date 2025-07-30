#gemini.py will handle the Gemini API interactions

#imports
from google import genai
import os
import dotenv

#Load dotenv for environment variables
dotenv.load_dotenv()

#create a client for the Gemini API
client = genai.Client(api_key=os.getenv('GENAI_API_KEY'))

#test a response
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Please Generate a recipe for a basic mexican dish"
)

print(response.text)