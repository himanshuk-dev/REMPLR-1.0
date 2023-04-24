from database import db
from database import db, connect_db

class MealPlan(db.Model):
    '''Model for meal plan table'''
    
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    meal_type = db.Column(db.String, nullable = False)
    meal_day = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('nutritionists.id', ondelete="CASCADE"))

    def __repr__(self):
        return f'<MealPlan {self.name}>'
