from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json
from datetime import datetime

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token, get_channel_subs
from db_func import create_user, add_news, get_news_from_db,delete_news_data,get_date_dif,get_dep_reg_data



@app.route("/get_leaderboard",methods=["GET"])
def get_leaderboard():
    from_time = request.args.get("from_time",None)
    to_time = request.args.get("to_time",None)
    if not from_time or not to_time:
        date = [datetime.now().strftime("%d.%m.%Y")]
    else:
        date = get_date_dif(from_time,to_time) 
    
    data = list(db.channel.find({},{"_id":0,"active":0}))
    for i in data:
        i["subs"] = get_channel_subs(i["channel_id"])
        dep_reg = get_dep_reg_data(i["channel_id"],date)
        dep = 0
        reg = 0
        for j in dep_reg:
            dep += dep_reg[j]["dep"]
            reg += dep_reg[j]["reg"]
        i["dep"] = dep
        i["reg"] = reg
    data.sort(key=lambda x:x['dep'],reverse=True)
    response = jsonify({"status":1,"data":data})
    return response



@app.route("/get_leaderboard_users",methods=["GET"])
def get_leaderboard_users():
    datas = list(db.users.find({},{"_id":0,"image":1,"mmr":1,"username":1}).sort("mmr", -1  ))
    for i in datas:
        if i.get("image",None) == None:
            i["image"] = "https://ik.imagekit.io/njtsu3vzq/image_j1BV8gOA4.jpg"
    response = jsonify({"status":1,"data":datas})
    return response

