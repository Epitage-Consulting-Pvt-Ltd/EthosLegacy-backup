#!/usr/bin/python3

import cv2
import os
from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

#face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")	#NL
cv2.startWindowThread()

picam2 = Picamera2()
#picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.configure(picam2.create_preview_configuration(main={"format": 'XBGR8888', "size": (640, 480)})) #NewLine
#config = picam2.create_preview_configuration(main={"size": (640, 480)}, lores={"size": (320, 240), "format": "YUV420"}) #NewLine
#picam2.configure(config) #NewLine

picam2.start()

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #faces = face_detector.detectMultiScale(grey, 1.1, 5)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5, minSize=(15, 15),flags = cv2.CASCADE_SCALE_IMAGE)	#NL

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)  #Changed Values from 0,255,0 to 10,159,255 , 2

    cv2.imshow("Camera", im)

cv2.destroyAllWindows()
