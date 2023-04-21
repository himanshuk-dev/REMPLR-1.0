from database import db
from models.nutritionist import Nutritionist
from models.ingredient import Ingredient

class Recipe(db.Model):
    '''Model for Recipes table'''
    
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable = True)
    serving = db.Column(db.Number, nullable = True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id', ondelete="CASCADE"), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('nutritionists.id', ondelete="CASCADE"))

    # Define one-to-many relationship between recipes and meal_plans
    meal_plan = db.relationship('meal_plans', backref='recipes')

    def __repr__(self):
        return f'<Recipe {self.name}>'