from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback

app = Flask(__name__)
app.app_context().push() 

# Connect database using sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///REMPLR'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "lounge-BARBICAN-3158!"

# Show debug toolbar
toolbar = DebugToolbarExtension(app)