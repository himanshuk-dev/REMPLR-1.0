from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
import database

app = Flask(__name__)
app.app_context().push() 

# Show debug toolbar
toolbar = DebugToolbarExtension(app)