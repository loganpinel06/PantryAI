#gemini.py will handle the Gemini API interactions

#imports
from google import genai
from . import genai_client

#test a response
response = genai_client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Please Generate a recipe for a basic mexican dish"
)

print(response.text)