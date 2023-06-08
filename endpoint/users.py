from datetime import datetime
from cdn import upload_file

from flask import request,jsonify, session
from flask_cors import cross_origin

from app import app
from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token,check_register_entity
from db_func import create_user, get_users_data,update_profile_info, delete_user_data,create_user_data, get_salary






# @app.before_request
# def before_request():...
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
    create_user_data(data)
    response = jsonify({"status":1,"message":"Successfully registered"}), 200
    return response
    

@app.route("/login", methods=["POST"])
def login():
    # Get the username and password from the request body
    data = request.get_json()
    username = data.get("username",None)
    pwd = data.get("password",None)
    if not username or not pwd:
        return jsonify({"status":0,"message":"Wrong creditales"})

    # Check if the username and password are correct
    data = db.users.find_one({"username": username, "pwd": pwd},{"_id":1,"position":1,"title":1,"channel_type":1})
    if data:
        data["time"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        if data is not None:
            # Generate a JWT token for the user
            token = generate_jwt_token(data)
            response = jsonify({"position":data["position"],"token":token})
            return response
    # Return an error if the username or password is incorrect
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/get_users",methods=["GET"])
def get_users():
    
    token = request.headers["token"]
    data = validate_jwt_token(token)
    channel_type = data["channel_type"]
    data = get_users_data(channel_type)
    response = jsonify({"status":1,"data":data})
    return response


@app.route("/get_profile_info",methods=["GET"])
def get_progile_info():
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data:
        rang = data.get("rang",0)
        reminder = round((data["mmr"] % 150) / 150,2) *100
        from_mmr = rang * 150
        to_mmr = from_mmr + 150 
        data["rang"] = rang
        data["reminder"] = reminder
        data["from_mmr"] = from_mmr
        data["to_mmr"] = to_mmr
        response = jsonify({"status":1,"data":data})
        return response
    return jsonify({"status":0}), 403


@app.route("/edit_profile_info",methods=["POST"])
def edit_profile_info():
    json_data = request.get_json()
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data:
        res = update_profile_info(data["username"],json_data)
        if res:
            response = jsonify({"status":1,"message":"Successfully updated"})
            return response
        response = jsonify({"status":0,"message":"Something worong during update"})
        return response
        
    return jsonify({"status":0}), 403



@app.route("/delete_user",methods=["DELETE"])
def delete_user():
    json_data = request.get_json()
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data and data["position"] < 3:
        username = json_data["username"]
        res = delete_user_data(username)
        if res:
            response = jsonify({"status":1,"message":"Successfully updated"})
            return response
        response = jsonify({"status":0,"message":"Something worong during update"})
        return response
    return jsonify({"status":0}), 404




@app.route("/create_user",methods=["POST"])
def create_user():
    json_data = request.get_json()
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data and data["position"] < 3:
        username = json_data["username"]
        check_username = db.users.find_one({"username":username},{"_id":0,"username":1})
        if check_username not in [None,{}]:
            return jsonify({"status":0}), 404
        pwd = json_data["pwd"]
        title = json_data["title"]
        position = json_data.get("position",3)
        project = json_data.get("project","")
        salary = get_salary(title)
        channel_type = data["channel_type"]
        res = create_user_data(username,pwd,title,position,project,salary,channel_type)
        if res:
            response = jsonify({"status":1,"message":"Successfully Added"})
            return response
        response = jsonify({"status":0,"message":"Something worong during update"})
        return response
        
    return jsonify({"status":0}), 404



@app.route("/edit_salary",methods=["POST"])
def edit_salary():
    json_data = request.get_json()
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data and data["position"] < 3:
        salary = json_data.get("salary",0)
        username = json_data.get("username",0)
        db.users.update_one({"username":username},{"$set":{"salary":int(salary)}})
        response = jsonify({"status":0,"message":"Something worong during update"})
        return response
        
    return jsonify({"status":0}), 404

@app.route("/edit_project",methods=["POST"])
def edit_project():
    json_data = request.get_json()
    token = request.headers["token"]
    data = validate_jwt_token(token)
    if data and data["position"] < 3:
        project = json_data.get("project","")
        username = json_data.get("username",0)
        db.users.update_one({"username":username},{"$set":{"project":project}})
        response = jsonify({"status":1})
        return response
        
    return jsonify({"status":0,"message":"Something worong during update"}), 404




@app.route("/edit_profile_photo",methods=["POST"])
def edit_profile_photo():
    token = request.headers["token"]
    data = validate_jwt_token(token)
    username = data["username"]
    if data:
        if file := request.files.get("Image",None):
            file.save("middle.png")
        else:
            return jsonify({"status":0,"message":"Does not exists image"}),400
        image_url = upload_file("middle.png")
        db.users.update_one({"username":username},{"$set":{"image":image_url}})
        return jsonify({"status":1,"message":"ok"})
    return jsonify({"status":0,"message":"Does not exists image"}),400