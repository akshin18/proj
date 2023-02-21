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
        "session": "",
        "pwd": data["pwd"],
        "project": data["project"],
        "created_time": datetime.now(),
        "updated_time": datetime.now()
    })
    return True


def add_news(title, text, color, hashtag):
    db.news.insert_one({
        "title": title,
        "text": text,
        "color": color,
        "hashtag": hashtag,
        "time": datetime.now().strftime("%H:%M"),
        "date": datetime.now().strftime("%d.%m"),
    })
    return True


def add_task(title, content, worker, manager, fine, minute, hour, date, feedback, _type, user_state=2):
    now = datetime.now()
    state = 0
    print(user_state)
    if user_state == 1:
        state = 1

    for i in worker.split(","):
        i = i.strip()
        worker_username = db.users.find_one({"_id":ObjectId(i)},{"username":1})["username"]
        db.tasks.insert_one({
            "title": title,
            "content": content,
            "worker": i,
            "worker_username":worker_username,
            "manager": manager,
            "fine": fine,
            "date": f"{date} {hour}:{minute}",
            "feedback": feedback,
            "created_time": now,
            "messages": "",
            "state": state,
            "type": _type
        })
    return True


def check_username(username):
    return db.users.find_one({"username": username})


def get_news_from_db():
    data = list(db.news.find({}, {}))
    return data


def get_users_data():
    data = list(db.users.find({}, {"_id": 0, "updated_time": 0}))
    return data


def delete_user(username):
    try:
        db.users.delete_one({"username": username})
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
    db.news.delete_one({"_id": ObjectId(f"{_id}")})
    return True


def update_profile_info(username, data):
    data = check_update_date(data)
    db.users.update_one({"username": username}, {"$set": data})
    return True


def add_market_data(image_url, name, price, content):
    db.market.insert_one({
        "url": image_url,
        "price": price,
        "name": name,
        "content": content
    })
    return True


def delete_market_data(_id):
    db.market.delete_one({"_id": ObjectId(f"{_id}")})
    return True


def buy_market_data(_id, user):
    code = generate_code()
    ttk = db.market.find_one({"_id": ObjectId(_id)}, {
                             "price": 1, "_id": 0})["price"]
    res = db.users.update_one({"username": user["username"], "ttk": {
                              "$gte": ttk}}, {"$inc": {"ttk": -ttk}})
    if res.raw_result["n"]:
        create_order(_id, user["username"], code)
        return code
    return None


def create_order(stuff_if, username, code):
    db.orders.insert_one({"username": username, "stuff_id": ObjectId(
        stuff_if), "complated": 0, "code": code})


def get_task_data(user_id):
    work = list(db.tasks.find({"worker": user_id}, {"created_time": 0}))
    manage = list(db.tasks.find({"manager": (user_id)}, {"created_time": 0}))
    for i in work:
        i["_id"] = str(i["_id"])
    for i in manage:
        i["_id"] = str(i["_id"])
    return work, manage


def confirm_task_data(user_id, _id):
    res = db.tasks.update_one({"worker": user_id, "state": {
                              "$in": [0, 3]}, "_id": ObjectId(_id)}, {"$set": {"state": 1}})
    print(res.raw_result)
    if res.raw_result["n"]:
        return True
    return False


def complate_task_data(user_id, _id, message):
    res = db.tasks.update_one({"worker": user_id, "state": 1, "_id": ObjectId(_id)}, {
                              "$set": {"state": 2, "messages": message}})
    if res.raw_result["n"]:
        return True
    return False


def reopen_task_data(user_id, _id):
    res = db.tasks.update_one(
        {"manager": (user_id), "state": 2, "_id": ObjectId(_id)}, {"$set": {"state": 3}})
    if res.raw_result["n"]:
        return True
    return False


def finish_task_data(user_id, _id):
    res = db.tasks.update_one(
        {"manager": (user_id), "state": 2, "_id": ObjectId(_id)}, {"$set": {"state": 4}})
    worker = db.tasks.find_one({"_id":ObjectId(_id)},{"worker":1})["woker"]
    db.users.update_one({"_id":ObjectId(worker)},{"$inc":{"mmr":35}})
    if res.raw_result["n"]:
        return True
    return False


def get_users_position_data(deeded_postion):
    res = list(db.users.find(
        {"position": deeded_postion}, {"_id": 1, "username": 1}))
    for i in res:
        i["_id"] = str(i["_id"])
    return res


def task_procces_check():
    r = list(db.tasks.find({}))
    for i in r:
        date = i["date"]
        now = datetime.now()
        compare_date = datetime.strptime(date, "%m %d %Y %H:%M")
        print(now)
        print(compare_date)
        if now > compare_date:
            fine_proccess(i)


def fine_proccess(data):
    fine = int(data["fine"])
    worker = data["worker"]
    fine_type = "tenge"
    if data["type"] == "MMR":
        fine_type = "mmr"
    db.users.update_many({"_id":ObjectId(worker)},
                            [
        {
            "$set": {
                f"{fine_type}": {   
                    "$max": [
                        0,
                        {
                            "$subtract": [
                                f"${fine_type}",
                                fine
                            ]
                        }
                    ]
                }
            }
        }
    ])
    db.tasks.delete_one({"_id":data["_id"]})