from app import app
from flask import request,jsonify
from add_func import check_register_entity
from db_func import create_user, add_news, get_news_from_db
from flask_cors import cross_origin

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token







@app.route("/post_news", methods=["POST"])
def post_news():
    # Get the username and password from the request body
    data = request.get_json()

    title = data.get("title",None)
    text = data.get("text",None)
    color = data.get("color",None)
    hashtag = data.get("hashtag",None)
    if add_news(title,text,color,hashtag):
    
        return jsonify({"status": 1}), 200
    return jsonify({"status": 0,"message":"Wrong detailes"}), 400


@app.route("/get_news", methods=["GET"])
@cross_origin()
def get_news2():
    news = get_news_from_db()
    response = jsonify({"status": 1,"data":news})
    return response


