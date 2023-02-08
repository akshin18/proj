from flask import jsonify,request
import os

from app import app









@app.route("/update_git",methods=["GET"])
def test():
    response = jsonify({"status":"Good"})
    os.system("git pull")
    os.system("pm2 restart proj")
    return response




@app.route("/test",methods=["GET"])
def test2():
    token = request.headers.get("token")
    print(token)
    response = jsonify({"status":token})
    return response



