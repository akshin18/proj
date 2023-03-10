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

def get_subscriber_count(channel,channel_id):
    response = channel.get("getSubscriberCount",channel_id)
    return response
def get_audience_gender(channel,channel_id):
    response = channel.get("getAudienceGender",channel_id)
    return response
def get_total_posts(channel,channel_id):
    response = channel.get("totalPosts",channel_id)
    return response
def get_recent_subscriber_count(channel,channel_id):
    # response = channel.get("recentSubscriberCount",channel_id)
    response = channel.get("todaySubscribers",channel_id)
    return response
def get_joined_by_date(channel,channel_id):
    response = channel.get("getJoinedByDate",channel_id)
    return response
def get_left_by_date(channel,channel_id):
    response = channel.get("getLeftByDate",channel_id)
    return response
def get_ref_and_dep(channel_id):
    data_from = datetime.now()
    api_key = get_key_for_statistic(channel_id)
    if api_key:
        try:
            data_to = (data_from - timedelta(days=14)).strftime("%Y-%m-%d")
            data_from = data_from.strftime("%Y-%m-%d")
            res = requests.get(f"http://pin-up.partners/api/{api_key}/statisticGeneral?from={data_to}&to={data_from}").json()["data"]
            reg,dep = res[0]["registration"],res[0]["firstDepositCount"]
            one_week_depo = sum([x["firstDepositCount"] for x in res[:7]])
            two_week_depo = sum([x["firstDepositCount"] for x in res])
            two_week_reg = sum([x["registration"] for x in res])
            return reg,dep,one_week_depo,two_week_depo,two_week_reg
        except Exception as e:
            print(e)
            return None,None,None,None,None
    return None,None,None,None,None
def get_key_for_statistic(channel_id):
    try:
        res = db.channel.find_one({"channel_id":channel_id},{"api":1}).get("api",None)
        return res
    except:
        return None
def check_data_appear(channel_id,channel_name):
    res = db.channel.find_one({"channel_id":channel_id})
    if not res:
        db.channel.insert_one({
            "channel_id":channel_id,
            "channel_name":channel_name,
            })

def main_schedule():
    loger_set("2")
    channel = Channel()
    data = get_channels(channel)
    channels = [x["channelId"] for x in data]
    db.channel.delete_many({"channel_id":{"$nin":channels}})
    now = int(datetime.now().timestamp())
    res = requests.get(f"http://146.0.78.143:5355/api/v1/statistics/tickets/time?projectId=bdac4609-9138-478e-9951-64038ce2fbab&date={now}",headers={"ApiKey":"q8B67Lh7hj2Ou"}).json()
    for i in data:
        channel_id = i["channelId"]
        channel_name = i["channelName"]
        check_data_appear(channel_id,channel_name)
        sub_count = get_subscriber_count(channel,channel_id)
        aud_gender = get_audience_gender(channel,channel_id)
        total_posts = get_total_posts(channel,channel_id)
        recent_sub_count = get_recent_subscriber_count(channel,channel_id)
        joined_by_date = get_joined_by_date(channel,channel_id)
        left_by_date = get_left_by_date(channel,channel_id)
        left_join_stat = []
        reg,dep,one_week,two_week,two_week_reg = get_ref_and_dep(channel_id)
        all_ticket = 0
        all_reply_time = 0
        for i,j,z,q in zip(joined_by_date,left_by_date,recent_sub_count,res):
            all_ticket += q["chatCount"]
            all_reply_time += q["averageSeconds"]
            left_join_stat.append({"time":i["time"],"join":i["value"],"left":j["value"],"subscribers":z["subscribers"],"ticket":q["chatCount"],"reply_time":q["averageSeconds"]})
        
        container = {
            "channel_id":channel_id,
            "channel_name":channel_name,
            "sub_count":sub_count,
            "aud_gender":aud_gender,
            "total_posts":total_posts,
            "left_join_stat":left_join_stat,
            "reg":reg,
            "dep":dep,
            "all_ticket":all_ticket,
            "all_reply_time":all_reply_time,
            "one_week_dep":one_week,
            "two_week_dep":two_week,
            "two_week_reg":two_week_reg
        
        }
        db.channel.update_one({"channel_id":channel_id},{"$set":container})


def salary_counter():
    loger_set("3")
    users = db.users.find({"position":{"$ne":1}})
    salary = db.adm_panel.find({})[0]
    for i in users:
        title = i["title"]
        _,dps,_,_,_ = get_ref_and_dep(i.get("channel_id",""))
        sal = salary.get(title,None)
        print(sal,dps,i.get("channel_id",""))
        if sal and dps:
            print("good")
            db.users.update_one({"username":i["username"]},{"$inc":{"tenge":int(((int(dps)**2)+int(sal))/int(salary["kpi"]))}})


def count_rang():
    res = db.users.find({})
    for i in res:
        mmr = i["mmr"]
        current_rang = i.get("rang",0)
        count_rang = mmr // 150
        if count_rang > current_rang:
            while count_rang > current_rang:
                current_rang += 1
                db.users.update_one({"_id":i["_id"]},{"$inc":{"ttk":1250},"$set":{"rang":current_rang}})
    loger_set("4")


if __name__ == "__main__":
    main_schedule()
    # salary_counter()