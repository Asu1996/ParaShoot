from imutils.video import WebcamVideoStream
from imutils.video import FPS
import numpy as np
import cv2
import imutils


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

if __name__ == '__main__':
    count=0
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()
    while True :
        '''count=(count+1)%6
        if count%6 != 0 :
            vs.grab()
            continue'''
        frame = vs.read()
        #frame = imutils.resize(frame, width=350)
        found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)        
        draw_detections(frame,found)
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
    cv2.destroyAllWindows()
