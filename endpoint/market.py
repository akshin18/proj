from app import app
from flask import request,jsonify
from add_func import check_register_entity
from db_func import get_market_data, add_market_data, delete_market_data, buy_market_data
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
    name = request.form.get("Name",None)
    price = request.form.get("Price",None)
    content = request.form.get("Content",None)
    if name and price and content:
        add_market_data(image_url, name, price, content)
        return jsonify({"status":1,"message":"ok"})
    return jsonify({"status":0,"message":"Does not exists main keys"}),400

@app.route("/delete_market",methods=["DELETE"])
def delete_market():
    data = request.get_json()
    if _id := data.get("_id"):
        data = delete_market_data(_id)
        response = jsonify({"status":1,"data":data})
        return response
    return jsonify({"status":0,"message":"Does not exists main keys"}),400



@app.route("/buy_market",methods=["POST"])
def buy_market():
    token = request.cookies["token"]
    data = request.get_json()
    if _id := data.get("_id"):
        user = validate_jwt_token(token)
        res = buy_market_data(_id,user)
        if res:
            response = jsonify({"status":1,"message":"Successfully bought"})
            return response,400
    response = jsonify({"status":0,"message":"Some error"})
    return response,400





