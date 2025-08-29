# <img src="app/static/images/PantryAI-Banner.png" width="100%" height="350px">

# 🍽️ About the App
Every find yourself stuck figuring out what to cook with the ingredients you have at home? PantryAI aims to help solve this problem.
This web application allows users to transfer their at home pantry to a digital space where Artificial Intelligence will seemlessly generate recipes based on the meal type selected. Built with Flask, Javascript, and Google Gemini API, the app enforces strong security practices and a clean user interface.

This app was created by Logan Pinel and completed on August 28th, 2025

# 💡 Features
- ### ⚡ **Dynamic DOM with Asynchronous JavaScript**
    - This app utilizes Asynchronous Javascript to fetch data from the backend and await its response before dynamically updating the DOM to enhance the user experience and limit the amount of page refreshes commonly found in basic Flask applications.
- ### 🔐 **Secure User Authentication**
    - Username and Password validation with Flask-WTF and Regepx to force strong inputs
    - Flask-Login for secure session handling
    - Configured Session Lifetime to ensure users are logged out after 30 minutes of inactivity
- ### 🛒 **Pantry Management**
    - Users can store and delete any ingredients they wish within the database
- ### 🤖 **Google Gemini API**
    - Integrated Google Gemini's 2.5 Flash-Lite Model to generate quality recipes for the user.
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

# ⚙️ Tech Stack
- ### **Core Technologies:**
    - Flask
    - JavaScript
    - HTML
    - SCSS
- ### **APIs**
    - Google Gemini API (2.5 Flash-Lite Model)
- ### **Flask Extensions:**
    - Flask-SQLAlchemy (ORM to create database models written in python)
    - Flask-WTF (create secure HTML form with CSRF protection)
    - Flask-Login (handle authentication logic)
    - Flask-Limiter (handle rate limiting to prevent brute force attacks)
- ### **Databases:**
    - PostgreSQL hosted on Supabase (stores all user, transaction, and balance data)
    - Redis hosted on Upstash (used for storing rate limiting data which is constantly being updated)

# 📁 Project Structure
```bash
├── README.md
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── gemini.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── CSS/
│   │   │   ├── styles.css
│   │   │   ├── styles.css.map
│   │   │   └── styles.scss
│   │   ├── JavaScript/
│   │   │   ├── pantry.js
│   │   │   └── saved-recipes.js
│   │   └── images/
│   │       ├── PaintryAI-Logo.PNG
│   │       └── PantryAI-Banner.png
│   └── templates/
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── base.html
│       └── main/
│           ├── pantry.html
│           └── saved-recipes.html
├── main.py
└── requirements.txt
```

# 🌐 Deployment
PantryAI is deployed via Render with the following production configurations:
- HTTPS enabled automatically with Render
- Gunicorn as the production WSGI server
- Logging to stdout for monitoring errors via Render Logs
Explore PantryAI here: https://pantryai-fbo8.onrender.com

# 💾 Run the Project Locally
### Clone the Repository
```
git clone https://github.com/loganpinel06/PantryAI
```
### Create a Python Virtual Environment in the local repository
macOS:
```
python3 -m venv env
```
Windows:
```
python -m venv env
```
### Activate the Virtual Environment
macOS:
```
source env/bin/activate
```
Windows:
```
env\Scripts\activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Setup a .env File With:
```
SECRET_KEY=your-secret-key
SUPABASE_CONNECTION_STRING=your-supabase-uri
REDIS_URI=your-redis-uri
```
1. Create a Secret Key which ensures session security and protection from attacks
    - Checkout this Article by [GeeksForGeeks](https://www.geeksforgeeks.org/python/secrets-python-module-generate-secure-random-numbers/) (see the section titled "Generating tokens")
2. Head over to [Supabase](https://supabase.com/) and create an account
    - Create a **FREE** project and follow the steps, **MAKE SURE TO SAVE PROJECT PASSWORD**, can store it in the .env file if you'd like
    - Next click on the **CONNECT** button at the top of the projects dashboard. Make sure the type is **URI** and copy the connection string into the .env
    - Now, replace the **'[YOUR-PASSWORD]'** part of the string with the password you saved earlier
3. Lastly head over to [Upstash](https://upstash.com/) and create an account
    - Create a Database and select the **FREE TIER**
    - Once on your new databases dashboard copy the url that starts with `redis://default:` and set it to the REDIS_URI in the .env file
    - Now replace the group of *'s with your databases token which can be copied from the same place as the uri string
### Run the Application
Navigate to main.py in the codebase and run the file!

# 🧠 What I Learned
This application marks the completion of my second full-stack web application with Flask. During my development I strengthened the skills I learned from developing Checkr-S which include: routing, HTTP methods, utilizing Flask extensions (Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Limiter), CSRF protection, rate limiting, building a secure authentication system, and integrating databases such as PostgreSQL (Supabase) and Redis (Upstash) all while mainting a modular code base.  
Additionally I expanded my knowledge and learned new skills which include:
- Learning JavaScript to facilitate a dynamic frontend, utilizing asynchronous programming (fetch/await) and DOM manipulation.
- Designing REST API routes on the backend that return JSON data which is handled with JavaScript instead of always returning a rendered HTML template.
- Integrating an external API and practice using Artificial Inteligence with the Google Gemini API.
- Creating a cleaner frontend experience by making use of HTML dialog modals.
Overall this is a project I am very proud as I was able to strengthen and refine my skill all while learning new high level topics and a whole new language which will help me throughout my career as a software engineer and full-stack developer.

# 📌 Future Development
With this application I learned a crucial new skill in JavaScript. This is something I really enjoyed learning and implementing and would like to continue developing skills in. For the future of PantryAI I would like to refactor the code base to be entirelly composed of JavaScript. This includes:
- Designing a backend with Node.js and Express.js
- Writing Database models with either MongoDB and Mongoose or PostgreSQL and Prisma.
- Constructing a new authentication system with Auth0 or OAuth.
- Utilizing a frontend framework like React to create a reusable, component-based architecture. 
