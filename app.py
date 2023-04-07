from flask import Flask, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from database import db, connect_db
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.mealplan import MealPlan
from models.user import User
from forms import RegisterForm, LoginForm

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


@app.route('/')
def home():
    '''Homepage'''
    if session.get('user_id'):    
        user_id = session['user_id']
        user = User.query.get_or_404(user_id)
        return render_template('index.html', user = user)
    else:
        return render_template('index.html')
    
@app.route('/Register', methods=['GET', 'POST'] )
def register():
    '''Show User registration form'''
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        new_user = User.register(username, email, first_name, last_name, password, role)
        
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html', form=form)
    
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''Show login form'''
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", 'primary')
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template('login.html', form = form)

@app.route('/users/<username>')
def user_info(username):
    '''Show user details page'''
    
    user = User.query.filter_by(username = username).first()
    return render_template('user_info.html', user = user)

@app.route('/logout')
def logout():
    '''Logout user'''
    
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/delete')
def delete_user(username):
    if(session['user_id']):
        user = User.query.filter_by(username = username).first()
        
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id')
        flash(f'User: {username} deleted!')
    return redirect('/')