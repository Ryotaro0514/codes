import RPi.GPIO as GPIO
import cv2
import time
import datetime
import requests
import numpy as np
import os
import pymongo
from google.cloud import bigquery



#LINEメッセージ送信の関数
def send_message(Discovery_time):
    url = "https://notify-api.line.me/api/notify" 
    token = "48Mb58nIDzAqMoAjoxNnMlAgJVNZVln11JOhd7T86ZN"
    headers = {"Authorization" : "Bearer "+ token}
    files = {'imageFile': open("image.jpg", "rb")}
    message =  (Discovery_time,"トイレ検知")
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload, files=files)


#BigQueryにデータ送信
def to_gbq(Discovery_time):
   client = bigquery.Client()
   table_id = 'supple-outlet-404309.SensorDataset2.PIRSensor' #プロジェクトID.データセットID.テーブルID

   rows_to_insert = [{'time': Discovery_time}]
   errors = client.insert_rows_json(table_id, rows_to_insert)
   if errors == []:
       print("New rows have been added.")
   else:
       print("Encountered errors while inserting rows: {}".format(errors))



#センサーを使う準備
PIR_OUT_PIN = 11    # pin11

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input

while True:
    if(GPIO.input(PIR_OUT_PIN) == GPIO.HIGH):
        #センサー検出時の処理
        print("1")
        
        #検出時間の取得
        dt_now = datetime.datetime.now()
        Discovery_time = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(Discovery_time)

        #Add MongoDB
        myclient = pymongo.MongoClient("mongodb+srv://ri514:ExfrFboIkE91FWOy@cluster0.opb7yue.mongodb.net/")
        mydb = myclient["Test"]
        mycol = mydb["date_test1"]

        #Insert a document
        mydoc = {"Date":Discovery_time}

        x = mycol.insert_one(mydoc)
        print (x)


        #query object/documents in a collection
        #myquery = {"name":"John"}
        #result = mycol.find(myquery)
        #for y in result:
        #   print (y)

        print("Message received:" + Discovery_time)

        #BigQueryにデータ送信
        to_gbq(Discovery_time)


        #5秒待機
        time.sleep( 5 )
        
        #カメラ画像を保存する
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("image.jpg", frame)
        cap.release()


        #LINEメッセージ送信
        send_message(Discovery_time)
        
        #90秒待機
        time.sleep( 90 )
        
    else:
        #センサー未検出時の処理
        print("0")
        time.sleep( 1 )
        
GPIO.cleanup()