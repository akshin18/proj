from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import create_user, add_news, get_news_from_db,delete_news_data




@app.route("/post_task", methods=["POST"])
def post_task():
    # Get the username and password from the request body
    data = request.get_json()

    title = data.get("title",None)
    text = data.get("text",None)
    color = data.get("color",None)
    hashtag = data.get("hashtag",None)
    if add_news(title,text,color,hashtag):
    
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400