from app import app
from flask import request,jsonify
from add_func import check_pars_files, check_proxy, save_proxy, get_pars_accouts_list,check_register_entity
from db_func import create_user, add_news, get_news_from_db

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

@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp

@app.before_request
def before_request():
    
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers[
            'Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        h['Content-Type'] = 'application/json'
        print("type of request" + str(type(h['Access-Control-Allow-Origin'])))
        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp
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
    print("Hello")
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
def get_news2():
    # news = get_news_from_db()
    # response = jsonify({"status": 1,"data":"da"})
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return "ok"