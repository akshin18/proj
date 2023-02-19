from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_task, get_task_data, confirm_task_data, complate_task_data, reopen_task_data, finish_task_data, get_users_position_data


#"
# state distribution
# 0 - created/available
# 1 - accepted/inprogress
# 2 - complated
# 3 - reopened
# 4 - finished
# 5 - rejected
# "

@app.route("/confirm_task",methods=["POST"])
def confirm_task():
    _id = request.get_json().get("_id")
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if confirm_task_data(user["_id"],_id):
        response = jsonify({"status":1,"message":"Successfully updated"})
        return response
    response = jsonify({"status":0,"message":"Some thing went error"})
    return response


@app.route("/complate_task",methods=["POST"])
def complate_task():
    data = request.get_json()
    _id = data.get("_id")
    message = data.get("message")
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if complate_task_data(user["_id"],_id,message):
        response = jsonify({"status":1,"message":"Successfully updated"})
        return response
    response = jsonify({"status":0,"message":"Some thing went error"})
    return response

    

@app.route("/reopen_task",methods=["POST"])
def reopen_task():
    _id = request.get_json().get("_id")
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if reopen_task_data(user["_id"],_id):
        response = jsonify({"status":1,"message":"Successfully updated"})
        return response
    response = jsonify({"status":0,"message":"Some thing went error"})
    return response


@app.route("/finish_task",methods=["POST"])
def finish_task():
    _id = request.get_json().get("_id")
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    if finish_task_data(user["_id"],_id):
        response = jsonify({"status":1,"message":"Successfully updated"})
        return response
    response = jsonify({"status":0,"message":"Some thing went error"})
    return response


@app.route("/get_task", methods=["GET"])
def get_task():
    # Get the username and password from the request body
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    work_data,manage_data = get_task_data(user["_id"])
    if work_data == []:
        work_data = [{}]
    if manage_data == []:
        manage_data = [{}]
    response = jsonify({"status":1,"work":work_data,"manage":manage_data})
    return response

@app.route("/post_task", methods=["POST"])
def post_task():
    # Get the username and password from the request body
    data = request.form
    title = data.get("title",None)
    content = data.get("content",None)
    worker = data.get("worker",None)
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    manager = user.get("_id")
    position = user.get("position")
    fine = data.get("fine",None)
    minute = data.get("minute",None)
    hour = data.get("hour",None)
    date = data.get("date",None)
    feedback = data.get("feedback",None)
    _type = data.get("type",None) 
    
    if add_task(title,content,worker,manager,fine,minute,hour,date,feedback,_type,user_state=position):
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400



@app.route("/get_workers",methods=["GET"])
def get_workers():
    token = request.headers.get("token")
    position = validate_jwt_token(token).get("position")
    if position <= 2:
        deeded_postion = position + 1
        data = get_users_position_data(deeded_postion)
        response = jsonify({"status":1,"data":data})
        return response
    response = jsonify({"status":0,"message":"You do not have permission"})
    return response