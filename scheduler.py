import requests
from config import db, PROJ_STATE

    
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
            url += f"?channelId={channel_id}"
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
    response = channel.get("recentSubscriberCount",channel_id)
    return response
def get_joined_by_date(channel,channel_id):
    response = channel.get("getJoinedByDate",channel_id)
    return response
def get_left_by_date(channel,channel_id):
    response = channel.get("getLeftByDate",channel_id)
    return response

def main_schedule():
    channel = Channel()
    data = get_channels(channel)
    for i in data:
        channel_id = i["channelId"]
        channel_name = i["channelName"]
        print(channel_id,channel_name)
        sub_count = get_subscriber_count(channel,channel_id)
        aud_gender = get_audience_gender(channel,channel_id)
        total_posts = get_total_posts(channel,channel_id)
        recent_sub_count = get_recent_subscriber_count(channel,channel_id)
        joined_by_date = get_joined_by_date(channel,channel_id)
        left_by_date = get_left_by_date(channel,channel_id)
        left_join_stat = []
        for i,j in zip(joined_by_date,left_by_date):
            left_join_stat.append({"time":i["time"],"join":i["value"],"left":j["value"]})
        
        container = {
            "channel_id":channel_id,
            "channel_name":channel_name,
            "sub_count":sub_count,
            "aud_gender":aud_gender,
            "total_posts":total_posts,
            "recent_sub_count":recent_sub_count,
            "left_join_stat":left_join_stat,
        
        }
        db.channel.update_one({"channel_id":channel_id},{"$set":container})
if __name__ == "__main__":
    main_schedule()