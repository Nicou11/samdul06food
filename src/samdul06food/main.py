from typing import Union
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pickle
import time
import os
import json

app = FastAPI()

origins = [
        "http://localhost:8006",
        "http://127.0.0.1:8899",
        "https://samdul06food.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

home_path = os.path.expanduser("~")
file_path = f"{home_path}/code/data/food/"
if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "n06"}

@app.get("/food")
def food(name: str):
    day = time.strftime('%Y-%m-%d')
    real_time = time.strftime('%Y-%m-%d %H:%M:%S')
    data = {"food": name, "time": real_time}
    with open(f"{file_path}/{day}", 'w') as f:
        json.dump(data, f)
    # 시간을 구함
    # 음식 이름과 시간을 csv 로 저장 -> /code/data/food.csv
    print("========================" + name )
    return {"food": name, "time": real_time}

food("pizza")

#@app.get("/food/save")
#def save(day):
