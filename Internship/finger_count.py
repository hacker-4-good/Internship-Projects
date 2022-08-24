import cv2
import time
import os
import HandTrackingModule as htm

wcam, hcam = 640, 480
ptime = 0
detector = htm.handTracker(detectionCon=0.75)

tipsID = [4,8,12,16,20]

# cap = cv2.VideoCapture("rtsp://admin:awicam6661@10.15.17.22:554/cam/realmonitor?channel=1&subtype=0")
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

while True:
    success, img = cap.read()
    img = detector.handsFinder(img)
    lmlist = detector.positionFinder(img, draw=False, handno=0)

    if len(lmlist)!=0:
        fingers = []

        if lmlist[tipsID[0]][1] < lmlist[tipsID[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmlist[tipsID[id]][2] < lmlist[tipsID[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        total_finger = fingers.count(1)
        cv2.putText(img, f'Finger: {int(total_finger)}', (100,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    ctime = time.time()
    fps = 1.0/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow('image', img)
    cv2.waitKey(1)