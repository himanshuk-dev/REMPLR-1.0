from database import db

class Ingredient(db.Model):
    '''Model for ingredients table '''
    
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable = True)
    
    # Define one-to-many relationship between ingredients and recipes
    recipe = db.relationship('recipes', backref='ingredients')

    def __repr__(self):
        return f'<Ingredient {self.name}>'