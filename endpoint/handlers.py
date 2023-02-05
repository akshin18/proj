from app import app
from flask import request,jsonify
from add_func import check_pars_files, check_proxy, save_proxy, get_pars_accouts_list,check_register_entity
from db_func import create_user, add_news, get_news_from_db
from flask_cors import cross_origin

from config import db, PROJ_STATE
from add_func import generate_jwt_token, validate_jwt_token


# @app.route("/check",methods=["POST"])
# def check_and_save():
#     if not check_pars_files(request.files):
#         response = jsonify({"status":0,"message":"Can not find needed files"})
#         return response

#     ip, port, user, pwd = request.form["ip"], request.form["port"], request.form["user"], request.form["pwd"] 
#     if not check_proxy(ip, port, user, pwd):
#         response = jsonify({"status":0,"message":"Invalid proxy"})
#         return response
    
#     save_proxy(request.files["json"].filename,{"ip":ip, "port":port,"suer":user, "pwd":pwd} )
#     request.files["json"].save(f'pars_account/{request.files["json"].filename}')
#     request.files["session"].save(f'pars_account/{request.files["session"].filename}')

#     response = jsonify({"status":1,"message":"OK"})
#     return response


# @app.route("/get_pars_account", methods=["GET"])
# def get_pars_account():
#     data = get_pars_accouts_list()
#     response = jsonify({"status":1,"message":"OK","data":data})
#     return response


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




