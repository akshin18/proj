from datetime import datetime,timedelta
from bson import ObjectId
# db.test.insert_one({"test":"test"})
# Mongo.db.users.insert_one({"name":"akshin","ok":"ol","as":1})
from config import db
from add_func import check_update_date, generate_code
import pymongo
import requests
import logging



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


def add_news(title, text, color, hashtag, image_url):
    db.news.insert_one({
        "title": title,
        "text": text,
        "color": color,
        "hashtag": hashtag,
        "time": datetime.now().strftime("%H:%M"),
        "date": datetime.now().strftime("%d.%m"),
        "image_url": image_url
    })
    return True


def add_task(title, content, worker, manager, fine, minute, hour, date, feedback, _type, user_state=2):
    now = datetime.now()
    state = 0
    if user_state == 1:
        state = 1

    for i in worker.split(","):
        i = i.strip()
        worker_username = db.users.find_one(
            {"_id": ObjectId(i)}, {"username": 1})["username"]
        db.tasks.insert_one({
            "title": title,
            "content": content,
            "worker": i,
            "worker_username": worker_username,
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
    data = list(db.users.find({"position": {"$gt": 1}}, {
                "_id": 0, "updated_time": 0}))
    return data


def delete_user(username):
    try:
        db.users.delete_one({"username": username})
        return True
    except:
        return False


def get_market_data():
    data = list(db.market.find({}))
    for i in data:
        i["_id"] = str(i["_id"])
    return data


def get_orders_data():
    data = list(db.orders.find({}))
    for i in data:
        i["_id"] = str(i["_id"])
        name_data = db.users.find_one({"_id": ObjectId(i["user_id"])}, {
                                      "first_name": 1, "last_name": 1, "middle_name": 1})
        name = name_data["first_name"]+"" + \
            name_data["last_name"]+"" + name_data["middle_name"]
        stuff_name = db.market.find_one(
            {"_id": i["stuff_id"]}, {"name": 1})["name"]
        i["name"] = name
        i["stuff_name"] = stuff_name
        i["stuff_id"] = str(i["stuff_id"])
    return data


def accept_order_data(_id):
    db.orders.update_one({"_id": ObjectId(_id)}, {"$set": {"complated": 1}})


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
    db.orders.delete_many({"stuff_id": ObjectId(f"{_id}")})
    return True


def delete_task_data(_id):
    db.tasks.delete_one({"_id": ObjectId(f"{_id}")})
    return True


def buy_market_data(_id, user):
    code = generate_code()
    ttk = db.market.find_one({"_id": ObjectId(_id)}, {
                             "price": 1, "_id": 0})["price"]
    res = db.users.update_one({"username": user["username"], "ttk": {
                              "$gte": int(ttk)}}, {"$inc": {"ttk": -int(ttk)}})
    if res.raw_result["n"]:
        create_order(_id, user["_id"], code)
        return code
    return None


def create_order(stuff_if, user_id, code):
    db.orders.insert_one({"user_id": user_id, "stuff_id": ObjectId(
        stuff_if), "complated": 0, "code": code})


def get_task_data(user_id, title=None):
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
    worker = db.tasks.find_one({"_id": ObjectId(_id)}, {"worker": 1})["worker"]
    db.users.update_one({"_id": ObjectId(worker)}, {"$inc": {"mmr": 35}})
    if res.raw_result["n"]:
        return True
    return False


def get_users_position_data(needed_postion, title: str = None):
    if needed_postion == 3:
        if title.startswith("treat"):
            res = list(db.users.find(
                {"position": needed_postion, "title": {"$in": ["trat_1", "trat_2", "trat_3"]}}, {"_id": 1, "username": 1}))
        else:
            res = list(db.users.find(
                {"position": needed_postion, "title": title}, {"_id": 1, "username": 1}))
    else:
        res = list(db.users.find(
            {"position": needed_postion}, {"_id": 1, "username": 1}))
    for i in res:
        i["_id"] = str(i["_id"])
    return res


def task_procces_check():
    r = list(db.tasks.find({"state": {"$lt": 4}}))
    for i in r:
        date = i["date"]
        now = datetime.now()
        try:
            compare_date = datetime.strptime(date, "%m %d %Y %H:%M")
            if now > compare_date:
                fine_proccess(i)
        except:
            pass


def fine_proccess(data):
    fine = int(data["fine"])
    worker = data["worker"]
    fine_type = "tenge"
    if data["type"] == "MMR":
        fine_type = "mmr"
    db.users.update_many({"_id": ObjectId(worker)},
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
    db.tasks.update_one({"_id": data["_id"]}, {"$set": {"state": 5}})
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    db.notifications.insert_one({"worker": ObjectId(
        worker), "message": f"Пропущенный Дедлайн", "value": -int(fine), "currency": fine_type, "date": now})


def delete_user_data(username):
    db.users.delete_one({"username": username})
    return True


def create_user_data(username, pwd, title, position,project,salary):
    now = datetime.now()
    db.users.insert_one(
        {
            "username": username,
            "pwd": pwd,
            "title": title,
            "first_name": "",
            "last_name": "",
            "middle_name": "",
            "birth_date": "",
            "email": "",
            "phone": "",
            "address": "",
            "position": int(position),
            "salary":salary,
            "mmr": 0,
            "ttk": 0,
            "tenge": 0,
            "session": "",
            "project": project,
            "created_time": now,
            "updated_time": now
        }
    )
    return True


def loger_set(a):
    db.loger.update_one({}, {"$set": {a: datetime.now()}})


def get_notifications_data(user_id):
    res = list(db.notifications.find(
        {"worker": ObjectId(user_id)}, {"_id": 0, "worker": 0}))
    return res


def add_dep_reg_data(date, dep, reg, channel_id):
    timestamp = int(datetime.strptime(date, "%d.%m.%Y").timestamp()) + 100
    db.dep_reg.delete_many({"channel_id":channel_id,"date":date})
    db.dep_reg.insert_one({"date": date, "dep": dep, "reg": reg,
                          "channel_id": channel_id, "timestamp": timestamp})


def get_dep_reg_data(channel_id, date):
    res = list(db.dep_reg.find(
        {"channel_id": channel_id, "date": {"$in":date}}, {"_id":0,"reg": 1, "dep": 1,"date":1},sort=[("_id", pymongo.DESCENDING)]))
    res_date = {}
    for i in res:
        dep = i["dep"]
        reg = i["reg"]
        if dep == '':
            dep = 0
        if reg == '':
            reg = 0
        if i["date"] in res_date.keys():
            res_date[i["date"]]["dep"] += int(dep)
            res_date[i["date"]]["reg"] += int(reg)
        else:
            res_date[i["date"]]= {"dep":int(dep),"reg":int(reg)}
    if res_date == {}:
        res_date = {date[0]:{"dep":0,"reg":0}}
    return res_date

def get_timestamp(from_time,to_time):
    return int(datetime.strptime(from_time,"%d.%m.%Y").timestamp())+30000,int(datetime.strptime(to_time,"%d.%m.%Y").timestamp())+30000

def get_stat(channel_id,from_timestamp,to_stimestamp):
    if from_timestamp == "" or to_stimestamp == "":
        logging.warning("SUDA")
        url = f"http://traffkillas.kz:5011/api/getCalendar?channelId={channel_id}"
    else:
        url = f"http://traffkillas.kz:5011/api/getCalendar?channelId={channel_id}&start={from_timestamp}&end={to_stimestamp}"
    payload={}
    headers = {
    'ApiKey': 'q8B67Lh7hj2Ou'
    }

    response = requests.get( url, headers=headers, data=payload)
    return response.json()


    # if not res:
    #     return 0, 0
    # return res["reg"], res["dep"]

def get_date_dif(from_time,to_time):
    d1 = datetime.strptime(from_time,"%d.%m.%Y")
    d2 = datetime.strptime(to_time,"%d.%m.%Y")
    logging.warning(f"{d1} : {from_time} || {d2} : {to_time}")
    diff = d2 - d1
    return [(d1 + timedelta(i)).strftime("%d.%m.%Y") for i in range(diff.days + 1)]

def get_statistic_name_data():
    res = list(db.channel.find({},{"_id":0,"channel_name":1,"channel_id":1}))
    return res

def prettier_stat(stat,dep_reg,ticket_average_time):
    date_dep = 0
    for i in stat:
        all_join = 0
        all_left = 0
        for j,l in zip(i["joined"],i["left"]):
            all_join += j["value"]
            all_left += l["value"]
        dep_reg_find = dep_reg.get(i["date"],{"dep":0,"reg":0})
        ticket_average_time_find = ticket_average_time.get(i["date"],{"ticket":0,"average":0})
        dep,reg = dep_reg_find["dep"],dep_reg_find["reg"]
        ticket,average = ticket_average_time_find["ticket"],ticket_average_time_find["average"]
        i["all_join"] = all_join
        i["all_left"] = all_left
        i["dep"] = dep
        date_dep += dep
        i["reg"] = reg
        i["ticket"] = ticket
        i["average"] = average
    return stat,date_dep



def get_ticket_average():
    r = requests.get()



def get_ticket_average(channel_id,from_timestamp,to_stimestamp):

    url = f"https://api2.traffkillas.kz/api/v1/statistics/tickets/range?channelId={channel_id}&start={from_timestamp}&end={to_stimestamp}"
    payload={}
    headers = {
    'ApiKey': 'q8B67Lh7hj2Ou'
    }
    response = requests.get( url, headers=headers, data=payload)
    if response.status_code != 200:
        return {datetime.now().strftime("%d.%m.%Y"):{"ticket":0,"average":0}}
    data = response.json()
    result = {}
    for i in data:
        result.update({i["date"]:{"ticket":i["ticketCount"],"average":i["answerTime"]["averageSeconds"]}})
    return result


def get_salary(title):
    print(title)
    res = db.adm_panel.find_one({},{"_id":0,title:1})
    return res[title]