import requests
from config import db, PROJ_STATE
from datetime import datetime
    
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
    data = datetime.now().strftime("%Y-%m-%d")
    api_key = get_key_for_statistic(channel_id)
    if api_key:
        res = requests.get(f"http://pin-up.partners/api/{api_key}/statisticGeneral?from={data}&to={data}").json()["data"][0]
        reg,dep = res["registration"],res["firstDepToReg"]
        return reg,dep
    return None,None
def get_key_for_statistic(channel_id):
    res = db.channel.find_one({"channel_id":channel_id},{"api":1}).get("api",None)
    return res
def check_data_appear(channel_id,channel_name):
    res = db.channel.find_one({"channel_id":channel_id})
    if not res:
        db.channel.insert_one({
            "channel_id":channel_id,
            "channel_name":channel_name,
            })

def main_schedule():
    channel = Channel()
    data = get_channels(channel)
    channels = [x["channelId"] for x in data]
    db.channel.delete_many({"channel_id":{"$nin":channels}})
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
        reg,dep = get_ref_and_dep(channel_id)
        for i,j,z in zip(joined_by_date,left_by_date,recent_sub_count):
            left_join_stat.append({"time":i["time"],"join":i["value"],"left":j["value"],"subscribers":z["subscribers"]})
        
        container = {
            "channel_id":channel_id,
            "channel_name":channel_name,
            "sub_count":sub_count,
            "aud_gender":aud_gender,
            "total_posts":total_posts,
            "left_join_stat":left_join_stat,
            "reg":reg,
            "dep":dep
        
        }
        db.channel.update_one({"channel_id":channel_id},{"$set":container})


if __name__ == "__main__":
    main_schedule()