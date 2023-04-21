from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json
from datetime import datetime

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_dep_reg_data, get_date_dif,get_dep_reg_data, get_stat, get_statistic_name_data, get_timestamp, prettier_stat
from cdn import upload_file
 

@app.route("/get_statistic",methods=["GET"])
def get_statistic():
    from_time = request.args.get("from_time",None)
    to_time = request.args.get("to_time",None)
    channel_id = request.args.get("channel_id",None)
    
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    position = user.get("position")
    if position  == 3:
        filter = {"channel_id":user.get("channel_id")}
    else:
        if channel_id != None:
            filter = {"channel_id":channel_id}
        else:
            filter = {}
    
    datas = list(db.channel.find(filter,{"_id":0,"name":1,"channel_id":1}))
    for data in datas:
        channel_id = data["channel_id"]
        if not from_time or not to_time:
            date = [datetime.now().strftime("%d.%m.%Y")]
            from_timestamp,to_stimestamp = "",""
        else:
            date = get_date_dif(from_time,to_time)
            from_timestamp,to_stimestamp = get_timestamp(from_time,to_time)
        dep_reg = get_dep_reg_data(channel_id,date)
        main_stat = get_stat(channel_id,from_timestamp,to_stimestamp)
        print(dep_reg)
        data ["stat"] = prettier_stat(main_stat,dep_reg)

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