import cv2
import numpy as np

cap = cv2.VideoCapture("apex_win.mp4")
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    #cv2.imshow('grayF',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break

cap.release()