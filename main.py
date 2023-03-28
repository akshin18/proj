from app import app,sched
from endpoint import users,news,market,test,tasks,adm_panel,statistic,leaderboard,notifications
from db_func import task_procces_check,loger_set
from scheduler import main_schedule, salary_counter, count_rang
import sys,os,time

if sys.platform != "win32":
    os.environ['TZ'] = 'Asia/Almaty' # set new timezone
    time.tzset()

def task_checker():
    loger_set("1")
    task_procces_check()

if __name__ == "__main__":
    sched.add_job(id="1",func=task_checker,trigger="interval",seconds=5)
    # sched.add_job(id="2",func=main_schedule,trigger="interval",seconds=10)
    sched.add_job(id="3",func=salary_counter,trigger="interval",days=1)
    sched.add_job(id="4",func=count_rang,trigger="interval",seconds=10)
    sched.start()
    app.run(host="0.0.0.0",port=3323,debug=True)