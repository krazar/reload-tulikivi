import cv2
import numpy as np
import os
import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected to broker")
    global Connected                #Use global variable
    Connected = True                #Signal connection
  else:
    print("Connection failed")

def readTulikiviLight(frame):
  lower = np.array([0, 120, 150])
  upper = np.array([255, 255, 255])

  mask = cv2.inRange(frame, lower, upper)
  nonZero = cv2.countNonZero(mask)
  height, width = mask.shape
  size = height * width
  ret = 0
  if (nonZero != 0):
    ret = nonZero * 100 / size
  return ret

def cropImage(frame):
  return frame[250:295, 445:491]

def closeImage(cap):
  cap.release()

def analyseImage(cap):
  ret, frame = cap.read()
  if (ret == True):
    image = cropImage(frame)
    ret = readTulikiviLight(image)
    return ret

def process(cap, mqttClient):
  result = analyseImage(cap)
  mqttClient.publish("tulikivi/state", result, qos=0, retain=True)

def mqttConnection(url, port, user, password):
  client = mqttClient.Client("Python")               #create new instance
  client.username_pw_set(user, password=password)    #set username and password
  client.on_connect= on_connect                      #attach function to callback
  client.connect(url, port=port)          #connect to broker

  client.loop_start()        #start the loop

  while Connected != True:    #Wait for connection
    time.sleep(0.1)
  return client;



def main():
  broker = os.environ['MQTT_URL']
  port = os.environ['MQTT_PORT']
  user = os.environ['MQTT_USER']
  password = os.environ['MQTT_PASS']
  url = os.environ['CAMERA_URL']
  client = mqttConnection(broker, port, user, password)
  cap = cv2.VideoCapture(url)
  process(cap, client)
  closeImage(cap)
  client.disconnect()
  client.loop_stop()

Connected = False   #global variable for the state of the connection

main()


