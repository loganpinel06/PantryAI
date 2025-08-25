# <img src="app/static/images/PantryAI-Banner.png" width="100%" height="350px">

# 🍽️ About the App
Every find yourself stuck figuring out what to cook with the ingredients you have at home? PantryAI aims to help solve this problem.
This web application allows users to transfer their at home pantry to a digital space where Artificial Intelligence will seemlessly generate recipes based on the meal type selected. Built with Flask, Javascript, and Google Gemini API, the app enforces strong security practices and a clean user interface.

This app was created by Logan Pinel and completed on August 24th, 2025

# 💡 Features
- ### ⚡ **Dynamic DOM with Asynchronous JavaScript**
    - This app utilizes Asynchronous Javascript to fetch data from the backend and dynamically update the DOM to enhance the user experience and limit the amount of page refreshes commonly found in basic Flask applications.
- ### 🔐 **Secure User Authentication**
    - Username and Password validation with Flask-WTF and Regepx to force strong inputs
    - Flask-Login for secure session handling
    - Configured Session Lifetime to ensure users are logged out after 30 minutes of inactivity
- ### 🛒 **Pantry Management**
    - Users can store and delete any ingredients they wish within the database
- ### 🤖 **Google Gemini API**
    - Integrated Google Gemini's Flash Lite 2.5 Model to generate quality recipes for the user.
    - The Model is prompted to take a list which stores the users pantry ingredients and the selected meal type (breakfast, lunch, dinner) and create 2 unique recipes.
    - Additionally the Model outputs its data in JSON format for easy integration with JavaScript
- ### 🗃️ **Saving Generated Recipes**
    - Users can save any AI generated recipes to the "Saved Recipes" page where any saved recipes are nicely displayed for users to go back and revisit if desired.
- ### 🚦 **Rate Limiting**
    - This app manages rate limiting using Flask-Limiter and Redis hosted on Upstash to store rate limit data in-memory
    - The addition of rate limiting helps protect the login route from brute-force attacks by limiting the number of requests an individual ip address can make at a time before getting locked for 5 minutes
- ### 💬 **HTML Dialog Modals**
    - One small but impactful feature is the use of HTML Dialog elements to display any generated recipe data.
    - This addition allows the webpage to focus in on the important information of the recipe and shadow all the background data seen on the page which provides a significantly better user experience on the application.