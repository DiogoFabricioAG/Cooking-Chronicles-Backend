import os
from flask import Flask,request,jsonify
from db import db_init
from ma import ma_init
from config import Config
from werkzeug.utils import secure_filename
from models import *
from schemas import *
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__) 
app.config.from_object(Config)
cors = CORS(app,origins=["http://localhost:5173"])

db_init(app)
ma_init(app)
migrate = Migrate(app, db)
# ------------------------------------------------- 

ROUTE_USERS = "/api/user/"
@app.route(ROUTE_USERS,methods=["GET"])
@cross_origin()
def index():
    if request.method == "GET":
        all_users =  UserModel.query.all()
        return UserSchema(many=True).jsonify(all_users)

@app.route(f"{ROUTE_USERS}create/",methods=["POST"])
@cross_origin()
def createuser():
    user = UserModel(username=request.json["user"],password=request.json["password"])
    db.session.add(user)
    db.session.commit()
    return 'Usuario creado'
@app.route(f"{ROUTE_USERS}login/",methods=["POST"])
@cross_origin()
def loginuser():
    user = UserModel.query.filter_by(username = request.json["username"]).first()
    if user:
        return UserSchema().jsonify(user)
    else:
        return "Usuario no encontrado", 404


