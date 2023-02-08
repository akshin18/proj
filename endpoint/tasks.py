from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_task, get_task_data, confirm_task_data, complate_task_data, reopen_task_data, finish_task_data


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
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    confirm_task_data(user["_id"])

@app.route("/complate_task",methods=["POST"])
def complate_task():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    complate_task_data(user["_id"])

@app.route("/reopen_task",methods=["POST"])
def reopen_task():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    reopen_task_data(user["_id"])

@app.route("/finish_task",methods=["POST"])
def finish_task():
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    finish_task_data(user["_id"])

@app.route("/get_task", methods=["GET"])
def get_task():
    # Get the username and password from the request body
    token = request.headers.get("token")
    user = validate_jwt_token(token)
    work_data,manage_data = get_task_data(user["_id"])
    response = jsonify({"status":1,"work":work_data,"manage":manage_data})
    return response

@app.route("/post_task", methods=["POST"])
def post_task():
    # Get the username and password from the request body
    data = request.get_json()

    title = data.get("title",None)
    content = data.get("content",None)
    worker = data.get("worker",None)
    manager = data.get("manager",None)
    fine = data.get("fine",None)
    minute = data.get("minute",None)
    hour = data.get("hour",None)
    feedback = data.get("feedback",None)
    
    if add_task(title,content,worker,manager,fine,minute,hour,feedback):
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400