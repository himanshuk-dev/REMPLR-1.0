from database import db
from models.nutritionist import Nutritionist
from models.ingredient import Ingredient

class Recipe(db.Model):
    '''Model for Recipes table'''
    
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey('nutritionists.id', ondelete="CASCADE"))

    # Define one-to-many relationship between ingredients and recipes
    ingredient = db.relationship('Ingredient', backref='recipes')
    meal_plans = db.relationship('MealPlan', backref='recipes')

    def __repr__(self):
        return f'<Recipe {self.name}>'