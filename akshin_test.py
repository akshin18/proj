from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/ts",methods=["GET"])
def gqw():
    return "QWE"



if __name__ == "__main__":
    app.run(host="0.0.0.0")