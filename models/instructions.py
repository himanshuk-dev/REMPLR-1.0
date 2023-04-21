from database import db
from models.recipe import Recipe

class Instructions(db.Model):
    '''Model for instructions table'''
    
    __tablename__ = 'instructions'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"))

    def __repr__(self):
        return f'<Recipe {self.name}>'