from app import app
from endpoint import users,news,market




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)