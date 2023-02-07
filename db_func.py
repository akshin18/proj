from datetime import datetime
from bson import ObjectId
# db.test.insert_one({"test":"test"})
# Mongo.db.users.insert_one({"name":"akshin","ok":"ol","as":1})
from config import db
from add_func import check_update_date, generate_code


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

def add_task(title,content,worker,fine,minute,hour,feedback):
    now = datetime.now()
    db.tasks.insert_one({
        "title":title,
        "content":content,
        "worker":worker,
        "fine":fine,
        "minute":minute,
        "hour":hour,
        "feedback":feedback,
        "created_time":now
    })
    return True
def check_username(username):
    return db.users.find_one({"username": username})


def get_news_from_db():
    data = list(db.news.find({},{}))
    return data


def get_users_data():
    data = list(db.users.find({},{"_id":0,"updated_time":0}))
    return data

def delete_user(username):
    try:
        db.users.delete_one({"username":username})
        return True
    except:
        return False

def get_market_data():
    data = list(db.market.find({}))
    print(data)
    for i in data:
        i["_id"] = str(i["_id"])
    return data


def delete_news_data(_id):
    db.news.delete_one({"_id":ObjectId(f"{_id}")})
    return True

def update_profile_info(username,data):
    data = check_update_date(data)
    db.users.update_one({"username":username},{"$set":data})
    return True


def add_market_data(image_url, name, price, content):
    db.market.insert_one({
        "url":image_url,
        "price":price,
        "name":name,
        "content":content
    })
    return True


def delete_market_data(_id):
    db.market.delete_one({"_id":ObjectId(f"{_id}")})
    return True

def buy_market_data(_id,user):
    code = generate_code()
    ttk = db.market.find_one({"_id":ObjectId(_id)},{"price":1,"_id":0})["price"]
    res = db.users.update_one({"username":user["username"],"ttk":{"$gte":ttk}},{"$inc":{"ttk":-ttk}})
    if res.raw_result["n"]:
        create_order(_id,user["username"],code)
        return code
    return None


def create_order(stuff_if,username,code):
    db.orders.insert_one({"username":username,"stuff_id":ObjectId(stuff_if),"complated":0,"code":code})


def get_task_data():
    data = list(db.tasks.find({},{"created_time":0}))
    for i in data:
        i["_id"] = str(i["_id"]) 
    return data