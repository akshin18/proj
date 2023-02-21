from app import app,sched
from endpoint import users,news,market,test,tasks
from db_func import task_procces_check

def task_checker():
    task_procces_check()

if __name__ == "__main__":
    sched.add_job(id="1",func=task_checker,trigger="interval",seconds=5)
    sched.start()
    app.run(host="0.0.0.0",port=5000,debug=True)