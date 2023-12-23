import RPi.GPIO as GPIO
import cv2
import time
import datetime
import requests
import numpy as np
import paho.mqtt.client as mqtt

###### Edit variables to your environment #######
broker_address = "test.mosquitto.org"     #MQTT broker_address
Topic = "piper-jp_ise"

# publish MQTT
print("creating new instance")
client = mqtt.Client("pub2") #create new instance

print("connecting to broker: %s" % broker_address)
client.connect(broker_address) #connect to broker


#LINEメッセージ送信の関数
def send_message(Discovery_time):
    url = "https://notify-api.line.me/api/notify" 
    token = "48Mb58nIDzAqMoAjoxNnMlAgJVNZVln11JOhd7T86ZN"
    headers = {"Authorization" : "Bearer "+ token}
    files = {'imageFile': open("image.jpg", "rb")}
    message =  (Discovery_time,"猫さん検知")
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload, files=files)

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
        Discovery_time = dt_now.strftime('%Y/%m/%d/%H/%M/%S')
        print(Discovery_time)

        print("Publishing message: %s to topic: %s" % (Discovery_time, Topic))
        client.publish(Topic,Discovery_time)
        
        #カメラ画像を保存する
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("image.jpg", frame)
        cap.release()
        
        #LINEメッセージ送信
        send_message(Discovery_time)
        
        #10秒待機
        time.sleep( 10 )
        
    else:
        #センサー未検出時の処理
        print("0")
        time.sleep( 1 )
        
GPIO.cleanup()