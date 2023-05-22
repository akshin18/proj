from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json
from datetime import datetime, timedelta

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_dep_reg_data, get_date_dif,get_dep_reg_data, get_stat, get_statistic_name_data, get_timestamp, prettier_stat, get_ticket_average
from cdn import upload_file
import logging
 

@app.route("/get_statistic",methods=["GET"])
def get_statistic():
    from_time = request.args.get("from_time",None)
    to_time = request.args.get("to_time",None)
    channel_id = request.args.get("channel_id",None)
    active = request.args.get("active",None)
    
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if user == None:
        return jsonify({"status":0}),404
    position = user.get("position")
    if position  == 3:
        filter = {"channel_id":user.get("project")}
    else:
        if channel_id != None:
            filter = {"channel_id":channel_id}
        else:
            filter = {}
    print(filter)
    
    if active != None:
        if active in ["True","true",True]:
            filter.update({"active":True})
        elif active in ["False","false",False]:
            filter.update({"active":False})
    # filter = {}
    
    datas = list(db.channel.find(filter,{"_id":0}))
    for data in datas:
        channel_id = data["channel_id"]
        if not from_time or not to_time:
            date = [datetime.now().strftime("%d.%m.%Y")]
            from_timestamp,to_stimestamp = int((datetime.now()).timestamp())+30000,int(datetime.now().timestamp())+30000
        else:
            date = get_date_dif(from_time,to_time)
            from_timestamp,to_stimestamp = get_timestamp(from_time,to_time)
        ticket_average_time = get_ticket_average(channel_id,from_timestamp,to_stimestamp)
        dep_reg = get_dep_reg_data(channel_id,date)
        weekly_dep_reg = get_dep_reg_data(channel_id,get_date_dif((datetime.now()-timedelta(days=3650)).strftime("%d.%m.%Y"),datetime.now().strftime("%d.%m.%Y")))
        middle_info = get_date_dif((datetime.now()-timedelta(days=3600)).strftime("%d.%m.%Y"),datetime.now().strftime("%d.%m.%Y"))
        weekly_ticket_from,weekly_ticket_to = get_timestamp(middle_info[0],middle_info[1])
        weekly_ticket_average_time = get_ticket_average(channel_id,weekly_ticket_from,weekly_ticket_to )
        weekly_dep = 0
        weekly_reg = 0
        weekly_ticket = 0
        dep_chart = []
        reg_chart = []
        for zi,i in enumerate(weekly_dep_reg):
            if zi <7:
                weekly_dep += weekly_dep_reg[i]["dep"]
                weekly_reg += weekly_dep_reg[i]["reg"]
            dep_chart.append(weekly_dep_reg[i]["dep"])
            reg_chart.append(weekly_dep_reg[i]["reg"])
        for i in weekly_ticket_average_time:
            weekly_ticket += weekly_ticket_average_time[i]["ticket"]
        main_stat = get_stat(channel_id,from_timestamp,to_stimestamp)
        data["stat"],date_dep = prettier_stat(main_stat,dep_reg,ticket_average_time)
        for i in data["stat"]:
            # stata = []
            # for zi,j in enumerate(i["joined"]):
            #     stata.append({"time":j["time"],"join":j["value"],"left":i["left"][zi]["value"],"sub":i["subscriberGraph"][zi]["subscribers"]})
            # i["statistic"] = stata
            i.pop("joined")        
            i.pop("left")        
            sub = i.pop("subscriberGraph")  
            i["sub"] = sub[-1]["subscribers"]

        data["percen"] =round(((sub[-1]["subscribers"]/sub[0]["subscribers"])-1)*100,2)
        data["subs"] = sub[-1]["subscribers"]
        data["weekly_dep"] = weekly_dep
        data["weekly_reg"] = weekly_reg
        data["weekly_ticket"] = weekly_ticket
        data["dep_chart"] = dep_chart
        data["reg_chart"] = reg_chart
        data["date_dep"] = date_dep
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



@app.route("/change_active",methods=["POST"])
def change_active():

    
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    data = request.get_json()
    active = data["active"]
    channel_id = data["channel_id"]
    print(active)
    db.channel.update_one({"channel_id":channel_id},{"$set":{"active":active}})
    return jsonify({"status":1,"message":"ok"})