# TO DO: Later : Change ingredients search and recipe search forms to WTForms 

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
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
except AttributeError:
    # this is used locally and used to run tests
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

# ===============================================
# ************** User related Routes ************
# ===============================================

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
    else:
        flash('Login first', "danger")
        return redirect('/')

# ===============================================
# ************ Search related Routes ************
# ===============================================

    
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
        url = f'{base_url}food/ingredients/search?query={search_query}&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()

        results = data['results']
        
        # Render the template with the results
        return render_template('search_ingredients.html',user = user, results = results)
        
    else:

        flash('Login first', "danger")
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
            
            url = f"{base_url}recipes/complexSearch?query={search_query}&diet=vegetarian&apiKey={api_key}"
            
        # Search by nutrients | user need to specify min/max carbs, min protein
        elif search_criteria == "nutrients":
            min_carbs = request.form["min_carbs"]
            max_carbs = request.form["max_carbs"]
            min_protein = request.form["min_protein"]
            url = f"{base_url}recipes/complexSearch?minCarbs={min_carbs}&maxCarbs={max_carbs}&minProtein={min_protein}&diet=vegetarian&apiKey={api_key}"
            
        else:
            # Handle invalid search criteria
            flash('Invalid search criteria', 'danger')

        # Make API request
        response = requests.get(url)
        results = response.json()
        # Render results page with data
        return render_template("search_recipes.html", user=user, results = results['results'])
    
    else:
        
        flash('Login first', "danger")
        
        return redirect('/')


@app.route('/recipes/save', methods=['POST']) 
def save_recipes():
    '''Route to save Recipes from search Results'''
    
    if session.get('nutritionist_id'):
        
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        
        # Get user input from form
        name = request.form["data_name"]
        
        new_recipe = Recipe(name = name, user_id = user_id)
        
        db.session.add(new_recipe)
        db.session.commit()
        
        flash(f'Saved Recipe: {name}', "success")
    
    else:
        flash('Login first', "danger")
    
    return redirect('/')

@app.route("/users/<username>/recipes")
def saved_recipes(username):
    '''Route to show saved Recipes'''
    
    if session.get('nutritionist_id'):
        
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        results = {'results': []}
        
        if(recipes):
            for recipe in recipes:
                url = f"{base_url}recipes/complexSearch?query={recipe.name}&diet=vegetarian&apiKey={api_key}"
                response = requests.get(url)
                result = response.json()
                results['results'].extend(result['results'])
                
        
            return render_template("saved_recipes.html", user=user, results = results['results'])
        
    
# ===============================================
# ************** Meal Planner Routes ************
# ===============================================

@app.route('/meal-planner')
def meal_planner():
    '''Render Meal Planner'''
    
    if session.get('nutritionist_id'):
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        
    else:
        flash('Login first', "danger")
        
    return render_template('meal_planner.html', user = user)
    
    
@app.route('/meal-plan-save', methods=['POST'])
def meal_plan_save():
    '''save Meal Plan to database'''
    
    if session.get('nutritionist_id'):
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",]
        meal = {'b':'Breakfast',
                'l': 'Lunch',
                'd': 'Dinner',
                's1': 'Snack1',
                's2': 'Snack2'}
        
        name = request.form.get('meal_plan_name')


        for key, value in request.form.items():
            if key != 'meal_plan_name':
                if key.startswith('b-'):
                    td_id = key.split('-')[1]
                    meal_type = meal['b']
                    meal_day = day[int(td_id)]
                    recipe_id = value
                    new_meal_plan = MealPlan(name = name, recipe_id = recipe_id, meal_type = meal_type, meal_day = meal_day, user_id = user_id)
                    db.session.add(new_meal_plan)
                    db.session.commit()
                elif key.startswith('s1-'):
                    td_id = key.split('-')[1]
                    meal_type = meal['s1']
                    meal_day = day[int(td_id)]
                    recipe_id = value
                    new_meal_plan = MealPlan(name = name, recipe_id = recipe_id, meal_type = meal_type, meal_day = meal_day, user_id = user_id)
                    db.session.add(new_meal_plan)
                    db.session.commit()
                elif key.startswith('d-'):
                    td_id = key.split('-')[1]
                    meal_type = meal['d']
                    meal_day = day[int(td_id)]
                    recipe_id = value
                    new_meal_plan = MealPlan(name = name, recipe_id = recipe_id, meal_type = meal_type, meal_day = meal_day, user_id = user_id)
                    db.session.add(new_meal_plan)
                    db.session.commit()
                elif key.startswith('s2-'):
                    td_id = key.split('-')[1]
                    meal_type = meal['s2']
                    meal_day = day[int(td_id)]
                    recipe_id = value
                    new_meal_plan = MealPlan(name = name, recipe_id = recipe_id, meal_type = meal_type, meal_day = meal_day, user_id = user_id)
                    db.session.add(new_meal_plan)
                    db.session.commit()
                
            
        flash('Saved Meal Plan', "success")
    
    else:
        flash('Login first', "danger")
    
    return redirect('/meal-planner')

@app.route("/users/<username>/meal-plans")
def saved_meal_plans(username):
    '''Route to show Saved Meal Plans'''
    
    if session.get('nutritionist_id'):
        
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

    
        names = MealPlan.query.with_entities(MealPlan.name).filter_by(user_id=user_id).distinct().all()
         
        # Convert the list of tuples to a list of strings
        mealplan_names = [name[0] for name in names]
        
        for meal_plan_name in mealplan_names:
            

            content = MealPlan.query.with_entities(MealPlan.meal_type, MealPlan.meal_day, MealPlan.recipe_id ).filter_by(name=meal_plan_name).distinct().all()
            meal_plan_content = [data for data in content]

            
            breakfast_list = [item for item in meal_plan_content if item[0] == 'Breakfast']
            snack1_list = [item for item in meal_plan_content if item[0] == 'Snack1']
            lunch_list = [item for item in meal_plan_content if item[0] == 'Lunch']
            snack2_list = [item for item in meal_plan_content if item[0] == 'Snack2']
            dinner_list = [item for item in meal_plan_content if item[0] == 'Dinner']
            
            def get_meal_storage(meal_list, meal_storage):
                for meal in meal_list:
                    if meal[1] == 'Monday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()
                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Monday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Tuesday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()
                        
                        if result:
                             
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Tuesday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Wednesday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()
                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Wednesday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Thursday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()

                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Thursday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Friday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()

                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Friday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Saturday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"

                        # Make API request
                        response = requests.get(url)
                        result = response.json()
                        
                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Saturday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                    if meal[1] == 'Sunday':
                        recipe_id = meal[2]

                        url = f"{base_url}recipes/{recipe_id}/information?apiKey={api_key}"
                        
                        # Make API request
                        response = requests.get(url)
                        result = response.json()
                        
                        if result:
                            recipe_name = result['title']
                            recipe_image = result['image']
                            meal_storage['Sunday'] = {'recipe_name': recipe_name, 'recipe_image': recipe_image}

                return meal_storage
            
            breakfast_storage = get_meal_storage(breakfast_list, {})
            snack1_storage = get_meal_storage(snack1_list, {})
            lunch_storage = get_meal_storage(lunch_list, {})
            snack2_storage = get_meal_storage(snack2_list, {})
            dinner_storage = get_meal_storage(dinner_list, {})
            return render_template('saved_meal_plans.html', breakfast = breakfast_storage ,snack1 = snack1_storage, lunch = lunch_storage, snack2 = snack2_storage, dinner = dinner_storage, user = user, days = days, meal_plan_name = meal_plan_name)    
        
        return render_template('saved_meal_plans.html', breakfast = breakfast_storage ,snack1 = snack1_storage, lunch = lunch_storage, snack2 = snack2_storage, dinner = dinner_storage, user = user, days = days)    