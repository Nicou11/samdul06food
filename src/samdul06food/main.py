from typing import Union
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pickle
import time
import os
import csv 
import pytz

app = FastAPI()

origins = [
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

#home_path = os.path.expanduser("~")
#file_path = "{home_path}/code/data/food.csv"  # local test용
file_path = "/code/data/food.csv"    # AWS 배포용
if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "n06"}

@app.get("/food")
def food(name: str):

    timezone = pytz.timezone('Asia/Seoul')
    korea = datetime.now(timezone) 
    day = time.strftime('%Y-%m-%d')
    real_time = korea.strftime('%Y-%m-%d %H:%M:%S')
    data = {"food": name, "time": real_time}

    import pymysql.cursors

    # Connect to the database
    connection = pymysql.connect(host=os.getenv("DB_IP", "localhost"),
                        port= int(os.getenv("DB_PORT", "33306")),
                        user='food',
                        password='1234',
                        db='fooddb',
                        cursorclass=pymysql.cursors.DictCursor)

    sql = "INSERT INTO foodhistory (username, foodname, dt) VALUES (%s, %s, %s)"

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, ('n06', name, real_time))
        connection.commit()
    

    #file_name = f"{file_path}/{day}.csv"
    file_name = "food.csv"
    
    # CSV 파일이 존재하는지 확인
    file_exists = os.path.isfile(file_path)
    
    # CSV 파일에 데이터 추가
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["food", "time"])
        writer.writerow(data)
    return {"food": name, "time": real_time}
