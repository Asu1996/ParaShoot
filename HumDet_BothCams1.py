# import the necessary packages
from imutils.video.pivideostream import PiVideoStream
from imutils.video import WebcamVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.object_detection import non_max_suppression
from time import sleep
import imutils
import cv2
import numpy as np
import os
import math
import thread
import RPi.GPIO as io
#from variables import pxC, wxC

def coord_finder(pC, wC):
    if not(len(pC) & len(wC)):
        return
    x=float(d*((pC[0][0]-200)*pHor-(200-wC[0][0])*wHor)/((pC[0][0]-200)*pHor+(200-wC[0][0])*wHor))
    y=float(250*d/((pC[0][0]-200)*pHor+(200-wC[0][0])*wHor))
    pz=float((pC[0][1]-150)/150*y*pVer)
    wz=float((wC[0][1]-150)/150*y*wVer)
    z=max(pz,wz)
    #print pC[0], wC[0]
    print x,y
    if x<0:
        dc_h=5+math.atan(-y/x)/3.14159*5
    elif x>0 :
        dc_h=10-math.atan(y/x)/3.14159*5
    else :
        dc_h=7.5
    if z>0 :
        dc_v=5+math.atan(y/z)/3.14159*5
    elif z<0:
        dc_v=10-math.atan(-y/z)/3.14159*5
    laser_h.ChangeDutyCycle(dc_h)
    laser_v.ChangeDutyCycle(dc_v)
    io.output(7,1)
    sleep(1)
    
    
'''def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)'''


if __name__ == '__main__':
    d=5.9
    pField=46
    wField=58
    pHor=float(4*math.tan(math.radians(pField/2))/5)
    pVer=float(3*math.tan(math.radians(pField/2))/5)
    wHor=float(4*math.tan(math.radians(wField/2))/5)
    wVer=float(3*math.tan(math.radians(wField/2))/5)
    #print math.degrees(math.atan(pHor)), math.degrees(math.atan(wHor))

    io.cleanup()
    io.setmode(io.BOARD)
    io.setup(7, io.OUT)
    io.output(7, 0)
    io.setup(11, io.OUT)
    io.setup(13, io.OUT)
    laser_h=io.PWM(11,50)
    laser_h.start(7.5)
    laser_v=io.PWM(13,50)
    laser_v.start(7.5)
        
    wd=400
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    wCam = WebcamVideoStream(src=0).start()
    pCam = PiVideoStream().start()
    sleep(2.0)
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
        pC=[((xA+xB)/2, 2*(yA+yB)/5) for (xA, yA, xB, yB) in pFine]
        wC=[((xA+xB)/2, 2*(yA+yB)/5) for (xA, yA, xB, yB) in wFine]
            #cv2.rectangle(pFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        for (xC, yC) in pC :
            cv2.circle(pFrame, (xC, yC), 2, (0, 255, 0), 2)    
        for (xC, yC) in wC :
            #cv2.rectangle(wFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.circle(wFrame, (xC, yC), 2, (0, 255, 0), 2)
        try:
            thread.start_new_thread(coord_finder, (pC, wC))
        except:
            print "Failure"
        cv2.imshow('PiCam',pFrame)
        cv2.imshow('WebCam',wFrame)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
    cv2.destroyAllWindows()
           
