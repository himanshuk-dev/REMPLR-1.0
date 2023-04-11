# TO DO: make a search page and display all the ingredients from search

from flask import Flask, render_template, flash, session, redirect, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from database import db, connect_db
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.mealplan import MealPlan
from models.nutritionist import Nutritionist
from models.client import Client
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.app_context().push() 

# Set app configuration using sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///REMPLR'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "lounge-BARBICAN-3158!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# Show debug toolbar
toolbar = DebugToolbarExtension(app)


# Base URL
base_url = 'https://api.spoonacular.com/'

# Image URL
image_url = 'https://spoonacular.com/cdn/ingredients_250x250/'

# API Key
api_key = "ac0e17f073af4388a91d75452dfa1051"


@app.route('/', methods =['GET', 'POST'])
def root():
    '''Homepage'''
    if session.get('nutritionist_id'):
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        
        return render_template('index.html', user = user)
    
    elif session.get('client_id'):
        user_id = session['client_id']
        user = Client.query.get_or_404(user_id)
        
        return render_template('index.html', user = user)
    
    else:
        return render_template('index.html')
    
@app.route('/search/ingredients', methods = ['POST'])
def search_ingredients():
    '''Route to show Ingredient search Results'''
    
    if session.get('nutritionist_id'):
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)

        api_key = "ac0e17f073af4388a91d75452dfa1051"
        search_query = request.form['search_query']
        url = f'{base_url}/food/ingredients/search?query={search_query}&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        results = data['results']

        # Render the template with the results
        return render_template('search_ingredients.html', user = user, results = results)
    
    elif session.get('client_id'):
        user_id = session['client_id']
        user = Client.query.get_or_404(user_id)
        
        api_key = "ac0e17f073af4388a91d75452dfa1051"
        search_query = request.form['search_query']
        url = f'{base_url}/food/ingredients/search?query={search_query}&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        results = data['results']
        
        # Render the template with the results
        return render_template('search_ingredients.html',user = user, results = results)
        
    else:
        return redirect('/')
    
    
@app.route("/search/recipes", methods=["POST"])
def search_recipes():
    '''Route to show Recipes search Results'''
    
    if session.get('nutritionist_id'):
        
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        
        # Get user input from form
        search_query = request.form["search_query"]
            
        search_criteria = request.form["search_criteria"]

        # Make API request based on search criteria
        
        # Search by Ingredients
        if search_criteria == "ingredients":
            url = f"{base_url}recipes/findByIngredients?ingredients={search_query}&apiKey={api_key}"
            
        # Search by nutrients | user need to specify min/max carbs, min protein
        elif search_criteria == "nutrients":
            min_carbs = request.form["min_carbs"]
            max_carbs = request.form["max_carbs"]
            min_protein = request.form["min_protein"]
            url = f"{base_url}/recipes/findByNutrients?minCarbs={min_carbs}&maxCarbs={max_carbs}&minProtein={min_protein}&apiKey={api_key}"
            
        else:
            # Handle invalid search criteria
            return "Invalid search criteria."

        # Make API request
        response = requests.get(url)
        results = response.json()

        # Render results page with data
        return render_template("search_recipes.html", user=user, results = results)
    
    else:
        return redirect('/')
    
    
@app.route('/Register', methods=['GET', 'POST'] )
def register():
    '''Show Registration page'''
    
    return render_template('register.html')
    

@app.route('/register/nutritionist', methods=['GET', 'POST'] )
def register_nutritionist():
    '''Show registration form for nutritionist'''
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # Check if the user already exists
        existing_user = Nutritionist.query.filter((Nutritionist.username == username) | (Nutritionist.email == email)).first()
        if existing_user:
            flash('The username or email is already taken', 'danger')
            return redirect('/register/nutritionist')
        
        # create the new user
        new_nutritionist = Nutritionist.register(username, email, first_name, last_name, password)
        db.session.add(new_nutritionist)
        db.session.commit()
        session['nutritionist_id'] = new_nutritionist.id 
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')
    
    return render_template('register_nutritionist.html', form=form)

@app.route('/register/client', methods=['GET', 'POST'] )
def register_client():
    '''Show registration form for client'''
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # Check if the user already exists
        existing_user = Client.query.filter((Client.username == username) | (Client.email == email)).first()
        if existing_user:
            flash('The username or email is already taken', 'danger')
            return redirect('/register/client')
        
        # create the new user
        new_client = Client.register(username, email, first_name, last_name, password)
        db.session.add(new_client)
        db.session.commit()
        session['client_id'] = new_client.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')
    
    return render_template('register_client.html', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''Show login form'''
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        nutritionist = Nutritionist.authenticate(username, password) 
        client = Client.authenticate(username, password)
        if nutritionist:
            flash(f"Welcome back, {nutritionist.username}!", 'primary')
            session['nutritionist_id'] = nutritionist.id
            return redirect('/')
        elif client:
            flash(f"Welcome back, {client.username}!", 'primary')
            session['client_id'] = client.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template('login.html', form = form)

@app.route('/users/<username>')
def user_info(username):
    '''Show user details page'''
    
    user = Nutritionist.query.filter_by(username = username).first() or Client.query.filter_by(username = username).first()
    return render_template('user_info.html', user = user)

@app.route('/logout')
def logout():
    '''Logout user'''
    if session.get('client_id'):    
        session.pop('client_id')
    elif session.get('nutritionist_id'):
        session.pop('nutritionist_id') 
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/delete')
def delete_user(username):
    '''Delete user account'''
    
    if(session['user_id']):
        user = Nutritionist.query.filter_by(username = username).first() or Client.query.filter_by(username = username).first()
        
        db.session.delete(user)
        db.session.commit()
        session.pop('nutritionist_id') or session.pop('client_id')
        flash(f'User: {username} deleted!')
    return redirect('/')


