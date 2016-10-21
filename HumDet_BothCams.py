# import the necessary packages
from imutils.video.pivideostream import PiVideoStream
from imutils.video import WebcamVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import cv2

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


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
        pFound, _ = hog.detectMultiScale(pFrame, winStride=(8,8), padding=(32,32), scale=1.05)
        wFound, _ = hog.detectMultiScale(wFrame, winStride=(8,8), padding=(32,32), scale=1.05) 
        draw_detections(pFrame,pFound)
        draw_detections(wFrame,wFound)
        cv2.imshow('PiCam',pFrame)
        cv2.imshow('WebCam',wFrame)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
cv2.destroyAllWindows()   
