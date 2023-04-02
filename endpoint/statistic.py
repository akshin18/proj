from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json
from datetime import datetime

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_dep_reg_data,get_dep_reg_data, get_statistic_name_data
from cdn import upload_file


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
        date = datetime.now().strftime("%d.%m.%Y")
        reg,dep = get_dep_reg_data(data["channel_id"],date)
        for i in data["left_join_stat"]:
            all_join += i["join"]
            all_left += i["left"]
        data["dep"] = dep
        data["reg"] = reg
        data["all_join"] = all_join
        data["all_left"] = all_left
        data["percen"] = round(((data["sub_count"]/data["left_join_stat"][0]["subscribers"])-1)*100,2)
    response = jsonify({"status":1,"data":datas})
    return response

@app.route("/get_statistic_name",methods=["GET"])
def get_statistic_name():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if not user:
        response = jsonify({"status":0,"message":"Error"}),404
        return response
    data = get_statistic_name_data()
    response = jsonify({"status":1,"data":data})
    return response

@app.route("/add_dep_reg",methods=["POST"])
def add_dep_reg():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    position = user.get("position")
    data = request.get_json()
    if position  != 1:
        response = jsonify({"status":0,"message":"Error"}),404
        return response
    date = data["date"]
    dep = data["dep"]
    reg = data["reg"]
    channel_id = data["channel_id"]
    add_dep_reg_data(date,dep,reg,channel_id)
    response = jsonify({"status":1,"data":"Sucessfully"})
    return response

@app.route("/add_project_image",methods=["POST"])
def add_project_image():
    if file := request.files.get("Image",None):
        file.save("middle.png")
    else:
        return jsonify({"status":0,"message":"Does not exists image"}),400
    image_url = upload_file("middle.png")
    channel_id = request.form.get("channel_id",None)
    db.channel.update_one({"channel_id":channel_id},{"$set":{"image":image_url}})
    return jsonify({"status":1,"message":"ok"})