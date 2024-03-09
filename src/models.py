from db import db

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(20),  nullable = False)
    mimetype = db.Column(db.Text, nullable=True)
    img = db.Column(db.Text, unique=True, nullable=True)
    description = db.Column(db.Text, nullable = True)
    education = db.Column(db.Text, nullable = True)
    age = db.Column(db.Integer, nullable = True)
    nationality = db.Column(db.Text, nullable = True)
    rank = db.Column(db.Text, nullable = True)
    speciality = db.Column(db.Text, nullable = True)
    count_recipes = db.Column(db.Integer, default = 0)
    comentrate = db.relationship("Comentrate",backref="comentrates")
    recipe = db.relationship("Recipe",backref="user")
    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password

recipe_ingredient = db.Table("recipe_ingredient",
    db.Column("recipe_id",db.Integer,db.ForeignKey("recipe.id")),
    db.Column("ingredient_id",db.Integer,db.ForeignKey("ingredient.id")),
)
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30),unique = True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30),unique = True)
    ingredient = db.relationship('Ingredient',secondary = recipe_ingredient, backref = "recipe")
    tag = db.relationship("Tag",backref="tags")
    user_model_id = db.Column(db.Integer,db.ForeignKey("user_model.id")) 
    comentrate = db.relationship("Comentrate",backref="comentrate")
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30),unique = True)
    recipe_id = db.Column(db.Integer,db.ForeignKey("recipe.id"))

class Comentrate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rate = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.Text,nullable = True)
    usermodel_id = db.Column(db.Integer,db.ForeignKey("user_model.id"))
    recipe_id = db.Column(db.Integer,db.ForeignKey("recipe.id"))

