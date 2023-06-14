import requests
from config import db, PROJ_STATE
from datetime import datetime, timedelta
from db_func import loger_set
from bson import ObjectId
    
class Channel:
    def __init__(self) -> None:
        
        self.url = "http://146.0.78.143:5011/api/"

        self.headers = {
        'ApiKey': 'q8B67Lh7hj2Ou'
        }

        self.s = requests.Session()

    def get(self,endpoint,channel_id=None):
        url = self.url + endpoint
        if channel_id :
            now = datetime.now().timestamp()
            url += f"?channelId={channel_id}&date={int(now)}"
        response = self.s.get(url,headers=self.headers)
        try:
            resp = response.json()
        except:
            resp = response.text
        finally:
            return resp

def get_channels(channel):
    response = channel.get( "getChannels")
    return response

def check_data_appear(channel_id,channel_name,channel_type):
    res = db.channel.find_one({"channel_id":channel_id})
    if not res:
        db.channel.insert_one({
            "channel_id":channel_id,
            "channel_name":channel_name,
            "image":"",
            "active":True,
            "channel_type":channel_type,
            })

def main_schedule():
    print("2")
    loger_set("2")
    channel = Channel()
    data = get_channels(channel)
    channels = [x["channelId"] for x in data]
    db.channel.delete_many({"channel_id":{"$nin":channels}})
    for i in data:
        channel_id = i["channelId"]
        channel_name = i["channelName"]
        channel_type = i["channelCategory"]
        check_data_appear(channel_id,channel_name,channel_type)


# def salary_counter():
#     loger_set("3")
#     users = db.users.find({"position":{"$ne":1}})
#     salary = db.adm_panel.find({})[0]
#     for i in users:
#         title = i["title"]
#         _,dps = get_ref_and_dep(i.get("channel_id",""))
#         sal = salary.get(title,None)
#         print(sal,dps,i.get("channel_id",""))
#         if sal and dps:
#             print("good")
#             db.users.update_one({"username":i["username"]},{"$inc":{"tenge":int(((int(dps)**2)+int(sal))/int(salary["kpi"]))}})


def count_rang():
    res = db.users.find({})
    for i in res:
        try:
            mmr = i["mmr"]
            current_rang = i.get("rang",0)
            count_rang = mmr // 150
            if count_rang > current_rang:
                while count_rang > current_rang:
                    current_rang += 1
                    db.users.update_one({"_id":i["_id"]},{"$inc":{"ttk":1250},"$set":{"rang":current_rang}})
        except:
            pass
    loger_set("4")


if __name__ == "__main__":
    main_schedule()
    # salary_counter()