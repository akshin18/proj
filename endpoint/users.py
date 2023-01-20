from app import app
from flask import request,jsonify
from add_func import check_register_entity
from db_func import create_user, get_user_data
from flask_cors import cross_origin

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token






@app.before_request
def before_request():...
    #     if PROJ_STATE == "DEBUG":
#         return
#     token = request.headers.get("Authorization")
#     if token is None and request.endpoint != "login":
#         return jsonify({"error": "No authorization header"}), 401

#     # Validate the JWT token
#     user = validate_jwt_token(token)
#     if user is not None:
#         return jsonify({"message": "Welcome, {}!".format(user["username"])})
#     else:
#         return jsonify({"error": "Invalid JWT token"}), 401


@app.route("/register",methods=["POST"])
def register():
    # data = request.json
    data = request.get_json()

    check_fields = check_register_entity(data)
    if not check_fields:
        response = jsonify({"status":0,"message":"Necessery field is not exists"}), 400
        return response
    create_user(data)
    response = jsonify({"status":1,"message":"Successfully registered"}), 200
    return response
    

@app.route("/login", methods=["POST"])
def login():
    # Get the username and password from the request body
    data = request.get_json()

    username = data["username"]
    pwd = data["password"]
    
    # Check if the username and password are correct
    user = db.users.find_one({"username": username, "pwd": pwd},{"_id":0,"username":1,"position":1})
    if user is not None:
        # Generate a JWT token for the user
        token = generate_jwt_token(user)
        return jsonify({"token": token})
    else:
        # Return an error if the username or password is incorrect
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/get_users",methods=["GET"])
def get_users():
    data = get_user_data()
    response = jsonify({"status":1,"data":data})
    return response