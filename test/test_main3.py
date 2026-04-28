import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

import os

from sqlalchemy import text, create_engine
# from utils.database import engine

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware, {
#         "allow_origins"
#     }
# )

if __name__ == "__main__":
    uvicorn.run("test_main3:app", host="0.0.0.0", port=5000, reload=True)