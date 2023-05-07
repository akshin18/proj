from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import create_user, add_news, get_news_from_db,delete_news_data



@app.route("/get_admin_panel",methods=["GET"])
def get_admin_panel():
    data = db.adm_panel.find_one({},{"_id":0})
    response = jsonify({"status":1,"data":data})
    return response


@app.route("/edit_admin_panel",methods=["POST"])
def edit_admin_panel():
    data = request.get_json()
    key = list(data.keys())[0]
    value = data[key]
    db.adm_panel.update_one({},{"$set":{key:int(value)}})
    db.users.update_many({"title":key},{"$set":{"salary":int(value)}})
    response = jsonify({"status":1,"message":"Succesfully updated"})
    return response


