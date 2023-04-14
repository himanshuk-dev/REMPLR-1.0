from database import db
from models.recipe import Recipe
from database import db, connect_db

class MealPlan(db.Model):
    '''Model for meal plan table'''
    
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    meal_type = db.Column(db.String, nullable = False)
    meal_day = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<MealPlan {self.name}>'
