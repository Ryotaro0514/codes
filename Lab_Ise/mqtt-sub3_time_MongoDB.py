
#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os
import pymongo
import time
import datetime

###########################################################
#####  Set constant values for MQTT broker   ##############

#BrokerAddress = "127.0.0.1"              # Local MQTT 
BrokerAddress = "mqtt.eclipseprojects.io"    # Cloud MQTT
MqttTopic = "piper-jp_ise"



###########################################################
#####  MongDB                   ###########################

#create a database,a collection
##########################
#In MongoDB, a database is not created until it gets content!
#MongoDB waits until you have created a collection (table)
#with at least one document (record) before it actually creates the database
#(and collection).
##########################

#In MongoDB, a collection is not created until it gets content!

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("piper-jp_ise")  # subするトピックを設定 

#Receiving Messages with the Paho MQTT Python Client
def on_message(client, userdata, message):  ### callback when get message from MQTT broker
    msg = str(message.payload.decode("utf-8"))

    #Add MongoDB
    myclient = pymongo.MongoClient("mongodb+srv://ri514:ExfrFboIkE91FWOy@cluster0.opb7yue.mongodb.net/")
    mydb = myclient["Test"]
    mycol = mydb["date_test"]

    #Insert a document
    mydoc = {"Date":msg}

    x = mycol.insert_one(mydoc)
    print (x)


    #query object/documents in a collection
    #myquery = {"name":"John"}
    #result = mycol.find(myquery)
    #for y in result:
    #   print (y)

    print("Message received:" + msg)






### Connect MQTT broker 
print("Connecting to MQTT broker:" + BrokerAddress)
client = mqtt.Client()               # Create new instance with Any clientID
client.on_connect = on_connect
client.on_message=on_message         # Attach function to callback


try:
    client.connect(BrokerAddress,keepalive=60)    #connect to broker
except:
    print("***** Broker connection failed *****")
    exit(1) 

### Subscribe ###
print("Subscribe topic:", MqttTopic)
client.subscribe(MqttTopic)          # Subscribe MQTT

### loop forever to wait a message ###
print("Waiting message...")
client.loop_forever()                # Loop forever
