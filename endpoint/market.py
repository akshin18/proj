from app import app
from flask import request,jsonify
from add_func import check_register_entity
from db_func import get_market_data
from flask_cors import cross_origin

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token





@app.route("/get_market",methods=["GET"])
def get_market():
    data = get_market_data()
    response = jsonify({"status":1,"data":data})
    return response


@app.route("/add_market",methods=["POST"])
def add_market():
    json = request.get_json()
    file = request.files
    print(file)
    return jsonify({"res":"ok"})