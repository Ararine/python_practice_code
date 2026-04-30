from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

app = FastAPI()

def job_function():
    print("scheduler test :", datetime.now())
    
scheduler = BackgroundScheduler()

scheduler.add_job(job_function, 'interval', seconds=3)

scheduler.start()
print("start scheduler", datetime.now())

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("end scheduler", datetime.now())
