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
    datas = list(db.channel.find({},{"_id":0}))
    for data in datas:
        data["date"] = datetime.now().strftime("%d.%m")
        all_join = 0
        all_left = 0
        all_subscribers = 0
        for i in data["left_join_stat"]:
            all_join += i["join"]
            all_left += i["left"]
            all_subscribers += i["subscribers"]
        data["all_join"] = all_join
        data["all_left"] = all_left
        data["all_subscribers"] = all_subscribers
    response = jsonify({"status":1,"data":datas})
    return response




