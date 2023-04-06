from flask import Flask

app = Flask(__name__)
app.app_context().push() 

# Connect database using sqlAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///REMPLR'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "lounge-BARBICAN-3158!"
