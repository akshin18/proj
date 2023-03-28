from app import app
from flask import request,jsonify
from add_func import check_register_entity
from flask_cors import cross_origin
from bson import json_util
import json

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from db_func import create_user, add_news, get_news_from_db,delete_news_data
from cdn import upload_file







@app.route("/post_news", methods=["POST"])
def post_news():
    # Get the username and password from the request body
    if file := request.files.get("Image",None):
        file.save("news.png")

    data = request.form
    image_url = upload_file("middle.png")
    title = data.get("title",None)
    text = data.get("text",None)
    color = data.get("color",None)
    hashtag = data.get("hashtag",None)
    if add_news(title,text,color,hashtag,image_url):
    
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400


@app.route("/get_news", methods=["GET"])
@cross_origin()
def get_news():
    news = get_news_from_db()
    json_data_with_backslashes = json_util.dumps(news)
    json_data = json.loads(json_data_with_backslashes)[::-1]
    response = jsonify({"status": 1,"data":json_data})
    return response



@app.route("/delete_news",methods=["DELETE"])
def delete_news():
    data = request.get_json()
    _id = data.get("_id",None)
    if _id:
        delete_news_data(_id)
        response = jsonify({"status":1})
        return response
    response = jsonify({"status":0,"message":"Problem with id"})
    return response
    