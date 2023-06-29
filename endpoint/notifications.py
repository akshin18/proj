from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import get_notifications_data




@app.route("/get_notifications", methods=["GET"])
@cross_origin()
def get_notifications():
    token = request.headers["token"]
    user = validate_jwt_token(token)
    user_id = user["_id"]
    data = get_notifications_data(user_id)
    response = jsonify({"status": 1,"data":data})
    return response