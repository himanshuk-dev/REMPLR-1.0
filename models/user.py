from database import db
from models.mealplan import MealPlan

class User(db.Model):
    '''Model for users table | Role defines: Nutritionists or Client'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'))

    # Define one-to-many relationship between nutritionists and clients
    clients = db.relationship('User', backref='nutritionist', remote_side=[id], lazy=True)
    
    # Define one-to-many relationship between user and meal plans
    meal_plan = db.relationship('MealPlan', backref='users')

    def __repr__(self):
        return f'<User {self.email}>'