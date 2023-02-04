from app import app
from flask import request,jsonify
from add_func import check_register_entity
from db_func import get_market_data, add_market_data
from flask_cors import cross_origin

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token
from cdn import upload_file


@app.route("/get_market",methods=["GET"])
def get_market():
    data = get_market_data()
    response = jsonify({"status":1,"data":data})
    return response


@app.route("/add_market",methods=["POST"])
def add_market():
    if file := request.files.get("Image",None):
        file.save("middle.png")
    else:
        return jsonify({"status":0,"message":"Does not exists image"}),400
    image_url = upload_file("middle.png")
    title = request.form.get("Title",None)
    price = request.form.get("Price",None)
    content = request.form.get("Content",None)
    if title and price and content:
        add_market_data(image_url, title, price, content)
        return jsonify({"status":1,"message":"ok"})
    print(title, price,content)
    return jsonify({"status":0,"message":"Does not exists main keys"}),400