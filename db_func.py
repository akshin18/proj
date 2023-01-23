from config import db
from datetime import datetime
from bson import ObjectId
# db.test.insert_one({"test":"test"})
# Mongo.db.users.insert_one({"name":"akshin","ok":"ol","as":1})


def create_user(data):
    check = check_username(data["username"])
    if check:
        return False
    db.users.insert_one({
        "username": data["username"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "middle_name": data["middle_name"],
        "birth_date": data["birth_date"],  # d.m.y
        "email": data["email"],
        "phone": data["phone"],
        "address": data["address"],
        "position": data["position"],  # Роль
        "mmr": 0,
        "ttk": 0,
        "tenge": 0,
        "session":"",
        "pwd":data["pwd"],
        "project":data["project"],
        "created_time": datetime.now(),
        "updated_time": datetime.now()
    })
    return True


def add_news(title,text,color,hashtag):
    db.news.insert_one({
        "title":title,
        "text":text,
        "color":color,
        "hashtag":hashtag,
        "time":datetime.now().strftime("%H:%M"),
        "date":datetime.now().strftime("%d.%m"),
    })
    return True
def check_username(username):
    return db.users.find_one({"username": username})


def get_news_from_db():
    data = list(db.news.find({},{}))
    return data


def get_user_data():
    data = list(db.users.find({},{"_id":0,"updated_time":0}))
    return data

def delete_user(username):
    try:
        db.users.delete_one({"username":username})
        return True
    except:
        return False

def get_market_data():
    data = list(db.market.find({},{"_id":0}))
    return data


def delete_news_data(_id):
    db.news.delete_one({"_id":ObjectId(f"{_id}")})
    return True