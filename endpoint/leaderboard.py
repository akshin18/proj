from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json
from datetime import datetime

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import create_user, add_news, get_news_from_db,delete_news_data



@app.route("/get_leaderboard",methods=["GET"])
def get_leaderboard():
    key = request.args.get("key",None)
    if not key :
        key = "dep"
    datas = list(db.channel.find({},{"_id":0}).sort( { "key": -1 } ))
    for data in datas:
        data["date"] = datetime.now().strftime("%d.%m")
        data["percen"] = round(((data["sub_count"]/data["left_join_stat"][0]["subscribers"])-1)*100,2)
    response = jsonify({"status":1,"data":datas})
    return response



@app.route("/get_leaderboard_users",methods=["GET"])
def get_leaderboard_users():
    datas = list(db.users.find({},{"_id":0,"image":1,"mmr":1}).sort( { "mmr": -1 } ))
    response = jsonify({"status":1,"data":datas})
    return response

