from pymongo import MongoClient


CONNECTION_STRING = "mongodb://akshin:qazxsw123?@146.0.78.143:27017/?directConnection=true&authSource=admin&appName=mongosh+1.6.1"
client = MongoClient(CONNECTION_STRING)
db = client["dev"]

JWT_SECRET_KEY = "de6be753cf4e8f3016ddf58a8013cdd0eef62bcfc630e65f3b1e26375eea81bc5ce20c1949137d2d"

PARS_DIR = "pars_account"
REGISTER_FIELDS = ["username", "first_name", "last_name", "middle_name",
                   "birth_date", "email", "phone", "address", "position", "pwd", "project"]
PROJ_STATE = "DEBUG"


PROFILE_UPDATE_DATA = ["username","pwd","birth_date","email","phone","address","first_name","last_name","middle_name"]