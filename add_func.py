import os
import json
import string
import random

import requests
import python_socks
from telethon.sync import TelegramClient
import jwt
from bson import ObjectId, json_util

from config import PARS_DIR, REGISTER_FIELDS, JWT_SECRET_KEY, db, PROFILE_UPDATE_DATA




def check_pars_files(files: dict):
    if not files.get('json', None):
        return False
    if not files.get('session', None):
        return False
    return True


def check_proxy(ip, port, user, pwd):
    print(ip, port, user, pwd)
    proxy = {
        "http": f"socks5://{user}:{pwd}@{ip}:{port}",
        "https": f"socks5://{user}:{pwd}@{ip}:{port}"
    }
    r = requests.get("http://httpbin.org/ip", timeout=5, proxies=proxy)
    if r.status_code == 200 and r.json().get("origin", None) == ip:
        return True
    return False


def save_proxy(json_name: str, data: dict):
    proxy_file_name = json_name.replace("json", "proxy")
    with open(f"{PARS_DIR}/{proxy_file_name}", "w")as f:
        f.write(json.dumps(data))


def get_pars_accouts_list():
    data_list = [x for x in os.listdir(f"{PARS_DIR}") if x.endswith("proxy")]
    data = []
    for i in data_list:
        with open(f"{PARS_DIR}/{i}")as f:
            res = json.loads(f.read())
            res["phone"] = i.replace(".proxy", "")
            data.append(res)
    return data


# def proccess(_id,_hash,phone):
#     proxy = (python_socks.ProxyType.SOCKS5,proxy,8000,True,"e7cXAR","r8VzYA")
#     api_id = _id
#     api_hash = _hash


#     try:
#         client = TelegramClient(f'{PARS_DIR}/{phone}', api_id, api_hash,proxy=proxy)
#         client.connect()


#         if client.is_connected() and client.is_user_authorized():
#             clients_list.append(client)
#             print("good")
#     except:
#         print("something went wrong")

def check_register_entity(data: dict):
    data_keys = list(data.keys())
    for i in REGISTER_FIELDS:
        if i not in data_keys:
            return False
    return True


def generate_jwt_token(data):
    # Generate the JWT token
    data["_id"] = str(data["_id"])
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm="HS512")
    print(token.decode())
    return token.decode()

def validate_jwt_token(token):
    claims = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS512"])
    try:
        # Decode the JWT token and verify its signature
        claims = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS512"])
        # Check if the user exists in the database
        if _id :=claims.get("_id",None):
            user = db.users.find_one({"_id":ObjectId(_id) },{"updated_time":0,"created_time":0})
            user["_id"] = str(user["_id"])
        else:
            return None
        if user is not None:
            return user
        else:
            return None

    except jwt.ExpiredSignatureError:
        # The JWT token has expired
        return None
    except jwt.InvalidTokenError:
        # The JWT token is invalid
        return None




def check_update_date(data):
    result = {}
    for i in data:
        if i in PROFILE_UPDATE_DATA and data[i]:
            result[i] = data[i]
    return result



def generate_code():
    list_of_elements = list(string.ascii_letters+string.digits)
    random.shuffle(list_of_elements)
    return "".join(list_of_elements[:15])


