# import the necessary packages
from imutils.video.pivideostream import PiVideoStream
from imutils.video import WebcamVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.object_detection import non_max_suppression
import imutils
import time
import cv2
import numpy as np
import os
from varbs import pxC, wxC

'''def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)'''


wd=400

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
wCam = WebcamVideoStream(src=0).start()
pCam = PiVideoStream().start()
time.sleep(2.0)
while True :
    pFrame = pCam.read()
    wFrame = wCam.read()
    pFrame = imutils.resize(pFrame, width=wd)
    wFrame = imutils.resize(wFrame, width=wd)
    pFound, _ = hog.detectMultiScale(pFrame, winStride=(8,8), padding=(8,8), scale=1.05)
    wFound, _ = hog.detectMultiScale(wFrame, winStride=(8,8), padding=(8,8), scale=1.05)
    pFound = np.array([[x, y, x + w, y + h] for (x, y, w, h) in pFound])
    wFound = np.array([[x, y, x + w, y + h] for (x, y, w, h) in wFound])
    pFine = non_max_suppression(pFound, probs=None, overlapThresh=1)
    wFine = non_max_suppression(wFound, probs=None, overlapThresh=1)
    pxC=[((xA+xB)/2, 2*(yA+yB)/5) for (xA, yA, xB, yB) in pFine]
    wxC=[((xA+xB)/2, 2*(yA+yB)/5) for (xA, yA, xB, yB) in wFine]
        #cv2.rectangle(pFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    for (xC, yC) in pxC :
        cv2.circle(pFrame, (xC, yC), 2, (0, 255, 0), 2)    
    for (xC, yC) in wxC :
        #cv2.rectangle(wFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        cv2.circle(wFrame, (xC, yC), 2, (0, 255, 0), 2)
    
    cv2.imshow('PiCam',pFrame)
    cv2.imshow('WebCam',wFrame)
    ch = 0xFF & cv2.waitKey(10)
    if ch == 27:
        break
cv2.destroyAllWindows()   
