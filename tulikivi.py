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
    client.subscribe("tulikivi/command")
    cap = cv2.VideoCapture(url)
    client.on_message = callbackMessage(cap)

  else:
    print("Connection failed")

def callbackMessage(cap):
  def on_message(client, userdata, message):
    print("message received " , str(message.payload.decode("utf-8")))
    process(cap, client)
  return on_message


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
  return frame[cropy, cropx]
#/return frame[201:231, 454:494]

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
  client.on_connect= on_connect
  client.connect(url, port=port)
  return client

broker = os.environ['MQTT_URL']
port = os.environ['MQTT_PORT']
user = os.environ['MQTT_USER']
password = os.environ['MQTT_PASS']
url = os.environ['CAMERA_URL']
cropx = os.environ['CROP-x']
cropy = os.environ['CROP-y']

client = mqttConnection(broker, port, user, password)
client.loop_forever()






