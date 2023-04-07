from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from database import db, connect_db
# from model import User, Ingredient, Recipe, MealPlan
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.mealplan import MealPlan
from models.user import User

app = Flask(__name__)
app.app_context().push() 

# Set app configuration using sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///REMPLR'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "lounge-BARBICAN-3158!"

connect_db(app)

# Show debug toolbar
toolbar = DebugToolbarExtension(app)