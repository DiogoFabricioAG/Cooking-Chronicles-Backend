from db import db
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30),unique = True)
    recipe_id = db.Column(db.Integer,db.ForeignKey("recipe.id"))


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(20),  nullable = False)
    image = db.Column(db.LargeBinary,nullable = True)
    description = db.Column(db.Text, nullable = True)
    education = db.Column(db.Text, nullable = True)
    age = db.Column(db.Integer, nullable = True)
    nationality = db.Column(db.Text, nullable = True)
    rank = db.Column(db.Text, nullable = True)
    linkface = db.Column(db.String(100),  nullable = True)
    linkinsta = db.Column(db.String(100),  nullable = True)
    linktik = db.Column(db.Text, nullable = True)
    count_recipes = db.Column(db.Integer, default = 0)
    comentrate = db.relationship("Comentrate",backref="comentrates")
    recipe = db.relationship("Recipe",backref="user")
    def __init__(self,username,password) -> None:
        self.username = username
        self.password = password
    
    def setvalues(self,data: dict):
        if data.get("username"):
            self.username = data.get("username")
        if data.get("age"):
            self.age = data.get("age")
        if data.get("nationality"):
            self.nationality = data.get("nationality")
        if data.get("description"):
            self.description = data.get("description")
        if data.get("education"):
            self.education = data.get("education")
        if data.get("speciality"):
            self.speciality = data.get("speciality")
        if data.get("linkinsta"):
            self.linkinsta = data.get("linkinsta")
        if data.get("linkface"):
            self.linkface = data.get("linkface")
        if data.get("linktik"):
            self.linktik = data.get("linktik")


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
    image = db.Column(db.LargeBinary,nullable = True)
    description = db.Column(db.Text, nullable = True)
    user_impressions = db.Column(db.Text, nullable = True)

    tag = db.relationship("Tags",backref="tags")
    ingredient = db.relationship('Ingredient',secondary = recipe_ingredient, backref = "recipe")
    user_model_id = db.Column(db.Integer,db.ForeignKey("user_model.id")) 
    comentrate = db.relationship("Comentrate",backref="comentrate")

class Comentrate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rate = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.Text,nullable = True)
    usermodel_id = db.Column(db.Integer,db.ForeignKey("user_model.id"))
    recipe_id = db.Column(db.Integer,db.ForeignKey("recipe.id"))
    def __init__(self,rate,comment,usermodel_id,recipe_id) -> None:
        self.rate = rate
        self.comment = comment
        self.usermodel_id = usermodel_id
        self.recipe_id = recipe_id

