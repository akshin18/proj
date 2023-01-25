from flask import jsonify
import os

from app import app









@app.route("/test",methods=["GET"])
def test():
    response = jsonify({"status":"Good"})
    os.system("git pull")
    os.system("pm2 restart proj")
    return response


@app.route("/test1",methods=["GET"])
def test2():
    response = jsonify({"status":"Good1"})
    return response