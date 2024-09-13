from typing import Union
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pickle
import time
import os
import csv 

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

    file_name = f"{file_path}/{day}.csv"
    
    # CSV 파일이 존재하는지 확인
    file_exists = os.path.isfile(file_name)
    
    # CSV 파일에 데이터 추가
    with open(file_name, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["food", "time"])
        # 파일이 처음 작성되는 경우 헤더를 추가
        if not file_exists:
            writer.writeheader()
        # 데이터 행 추가
        writer.writerow(data)
    print("========================" + name )
    return {"food": name, "time": real_time}
    # 시간을 구함
    # 음식 이름과 시간을 csv 로 저장 -> /code/data/food.csv

#food("chicken")
