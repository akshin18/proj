from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import add_task, get_task_data




@app.route("/get_task", methods=["GET"])
def get_task():
    # Get the username and password from the request body
    print("hello")
    data = get_task_data()
    print(data)
    response = jsonify({"status":1,"data":data})
    return response

@app.route("/post_task", methods=["POST"])
def post_task():
    # Get the username and password from the request body
    data = request.get_json()

    title = data.get("title",None)
    content = data.get("content",None)
    worker = data.get("worker",None)
    fine = data.get("fine",None)
    minute = data.get("minute",None)
    hour = data.get("hour",None)
    feedback = data.get("feedback",None)
    
    if add_task(title,content,worker,fine,minute,hour,feedback):
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400