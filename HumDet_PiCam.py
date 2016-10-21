# import the necessary packages
from imutils.video.pivideostream import PiVideoStream
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

# initialize the camera and stream
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
vs = PiVideoStream().start()
time.sleep(2.0)
 
# loop over some frames...this time using the threaded stream
while True :
        '''count=(count+1)%3
        if count%3 != 0 :
            vs.skip()
            continue'''
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)        
        draw_detections(frame,found)
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
cv2.destroyAllWindows()
vs.stop()
