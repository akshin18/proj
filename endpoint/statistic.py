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



@app.route("/get_statistic",methods=["GET"])
def get_statistic():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    position = user.get("position")
    filter = {}
    if position  == 3:
        filter = {"channel_id":user.get("channel_id")}
    datas = list(db.channel.find(filter,{"_id":0}))
    for data in datas:
        data["date"] = datetime.now().strftime("%d.%m")
        all_join = 0
        all_left = 0
        for i in data["left_join_stat"]:
            all_join += i["join"]
            all_left += i["left"]
        data["all_join"] = all_join
        data["all_left"] = all_left
        print(data["left_join_stat"][0])
        data["percen"] = round(((data["sub_count"]/data["left_join_stat"][0]["subscribers"])-1)*100,2)
    response = jsonify({"status":1,"data":datas})
    return response




