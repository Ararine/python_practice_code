from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone="Asia/Seoul")

def logic1():
    print(datetime.now(), "logic1 start!!")
    print(datetime.now(), "logic1 end!!")

def cron_test1():
    print(datetime.now(), "cron test1 start!!")
    logic1()
    print(datetime.now(), "cron test1 start!!")
    

def logic2():
    print(datetime.now(), "logic2 start!!")
    print(datetime.now(), "logic2 end!!")

def cron_test2():
    print(datetime.now(), "cron test2 start!!")
    logic2()
    print(datetime.now(), "cron test2 end!!")

def start_scheduler():
    scheduler.add_job(
        cron_test1,
        trigger="cron",
        hour=10,
        minute=15,
        id="cron_test1",
        replace_existing=True,  # id가 겹칠시 덮어쓰기 할 지 여부 설정
        max_instances=1,        # 하나의 job 이 동시에 몇 개까지 실행될 수 있는지 설정
        coalesce=True,          # 밀린 실행들을 각각 실행할지(False), 하나로 합쳐 실행할지(True) 설정
        misfire_grace_time=60,  # 스케줄 시간이 초과했을 때, 늦게 실행을 허용해주는 시간 설정
    )
    
    scheduler.add_job(
        cron_test2,
        trigger="cron",
        hour=10,
        minute=16,
        id="cron_test2",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60
    )
    
    scheduler.start()
    
def end_scheduler():
    print(datetime.now(), "end_scheduler start!!")
    scheduler.shutdown(wait=False)
    print(datetime.now(), "end_scheduler end!!")

# 시작과 종료의 로직을 하나의 함수로 관리하게 해줌
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("### hello ###")
    start_scheduler()

    yield
    
    print("### end ###")
    end_scheduler()
    
app = FastAPI(lifespan=lifespan)


