from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler


app = Flask(__name__)
sched = APScheduler()
CORS(app,supports_credentials=True)
