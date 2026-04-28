import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import db_test_api
from exceptions.handlers import register_exception_handlers

app = FastAPI()

# 1. 설정
register_exception_handlers(app)

# 2. 라우터        
app.include_router(db_test_api.router)


# pydantic 공부 후 schema로 받는거 테스트

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)