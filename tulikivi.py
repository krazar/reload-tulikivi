import cv2
import numpy as np
import os 

url = os.environ['CAMERA_URL']
cap = cv2.VideoCapture(url);
ret, frame = cap.read()


if (ret == True):

  frame = frame[250:295, 445:491]


  lower = np.array([210, 183, 209])
  upper = np.array([255, 255, 255])

  mask = cv2.inRange(frame, lower, upper)
  nonZero = cv2.countNonZero(mask)

  height, width = mask.shape
  size = height * width

  if (nonZero == 0):
    print(0)
  else:
    print(nonZero / size)

  cap.release()



