from io import BytesIO
from flask import Flask,request,jsonify,send_file
from db import db_init
from ma import ma_init
from config import Config
from models import *
from schemas import *
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_uploads import UploadSet, IMAGES, configure_uploads
from PIL import Image
app = Flask(__name__) 
app.config.from_object(Config)
cors = CORS(app,origins=["http://localhost:5173"])

db_init(app)
ma_init(app)

migrate = Migrate(app, db)
# ------------------------------------------------- 

ROUTE_USERS = "/api/user/"
ROUTE_RECIPES = "/api/recipes/"
# ------------------------------------------------- 
@app.route('/api/user/<int:user_id>/image', methods=['GET'])
def get_user_image(user_id):
    user = UserModel.query.get(user_id)
    if not user or not user.image:
        return jsonify({"message": "User or image not found"}), 404
    image = Image.open(BytesIO(user.image))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    img_io = BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
@app.route(f'{ROUTE_RECIPES}<int:recipe_id>/image', methods=['GET'])
def get_recipe_image(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    print(recipe)
    if not recipe or not recipe.image:
        return jsonify({"message": "User or image not found"}), 404
    image = Image.open(BytesIO(recipe.image))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    img_io = BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route(ROUTE_USERS,methods=["GET"])
@cross_origin()
def index():
    all_users =  UserModel.query.all()
    print(all_users)
    return UserSchema(many=True).jsonify(all_users)
@app.route(ROUTE_RECIPES,methods=["GET"])
@cross_origin()
def recipes():
    all_recipes =  Recipe.query.all()
    return RecipeSchema(many=True).dump(all_recipes)
@app.route(f"{ROUTE_RECIPES}best/<int:id>",methods=["GET"])
@cross_origin()
def bestrecipes(id):
    my_best_recipes =  Recipe.query.filter_by(user_model_id = id)[0:3]
    return RecipeSchema(many=True).dump(my_best_recipes)
@app.route(f"{ROUTE_USERS}<int:id>",methods=["GET"])
@cross_origin()
def userbyid(id):
    user = UserModel.query.filter_by(id=id).first()
    return UserSchema().jsonify(user)

@app.route(f"{ROUTE_USERS}create/",methods=["POST"])
@cross_origin()
def createuser():
    user = UserModel(username=request.json["user"],password=request.json["password"])
    db.session.add(user)
    db.session.commit()
    return 'Usuario creado'
@app.route(f"{ROUTE_RECIPES}create/",methods=["POST"])
@cross_origin()
def createrecipe():
    recipe = Recipe()
    user = UserModel.query.filter_by(id=int(request.values.get("id_user"))).first()

    recipe.name = request.values.get("name")
    recipe.description = request.values.get("description")
    recipe.user_impressions = request.values.get("user_impressions")
    recipe.image = request.files.get("image").read()
    recipe.user_model_id = user.id
    db.session.add(recipe)
    db.session.commit()
    return 'Receta creada'
@app.route(f"{ROUTE_USERS}edit/<int:id>/",methods=["PUT"])
@cross_origin()
def edituser(id):
    user = UserModel.query.filter_by(id=id).first()
    user.setvalues(request.values)
    user.image = request.files.get("image").read()
    db.session.commit()
    return 'Usuario editado'
@app.route(f"{ROUTE_USERS}login/",methods=["POST"])
@cross_origin()
def loginuser():
    user = UserModel.query.filter_by(username = request.json["username"], password = request.json["password"]).first()
    if user:
        return UserSchema().jsonify(user)
    else:
        return "Usuario no encontrado", 404


