import cv2
import numpy as np
import os
import time


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

def process(cap):
  result = analyseImage(cap)
  print(result)


def main():
  url = os.environ['CAMERA_URL']
  cap = cv2.VideoCapture(url)
  process(cap)
  time.sleep(5)
  closeImage(cap)

main()


