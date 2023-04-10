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


@app.route('/', methods =['GET', 'POST'])
def root():
    '''Homepage'''
    if session.get('nutritionist_id'):
        user_id = session['nutritionist_id']
        user = Nutritionist.query.get_or_404(user_id)
        if request.method == 'POST':
            api_key = "ac0e17f073af4388a91d75452dfa1051"
            search_query = request.form['search_query']
            url = f'https://api.spoonacular.com/food/ingredients/search?query={search_query}&apiKey={api_key}'
            response = requests.get(url)
            data = response.json()
            # Extract name and image of first result
            if data['totalResults'] > 0:
                first_result = data['results'][0]
                name = first_result['name']
                image = first_result['image']
            else:
                name = 'No results found'
                image = ''
            # Render the results template with the name and image            
            return render_template('index.html', user = user, name=name, image=image)
        
        return render_template('index.html', user = user)
    
    elif session.get('client_id'):
        user_id = session['client_id']
        user = Client.query.get_or_404(user_id)
        
        if request.method == 'POST':
            api_key = "ac0e17f073af4388a91d75452dfa1051"
            search_query = request.form['search_query']
            url = f'https://api.spoonacular.com/food/ingredients/search?query={search_query}&apiKey={api_key}'
            response = requests.get(url)
            data = response.json()
            # Extract name and image of first result
            if data['totalResults'] > 0:
                first_result = data['results'][0]
                name = first_result['name']
                image = first_result['image']
            else:
                name = 'No results found'
                image = ''
            # Render the results template with the name and image            
            return render_template('index.html', user = user, name=name, image=image)
        
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
            return redirect('/Register/nutritionist')
        
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
            return redirect('/Register/client')
        
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


