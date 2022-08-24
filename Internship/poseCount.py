import cv2
import time
import mediapipe as mp
import math
import numpy as np

mpDraw = mp.solutions.drawing_utils
mpHolistic = mp.solutions.holistic
holistic = mpHolistic.Holistic(min_detection_confidence=0.9, min_tracking_confidence=0.9)

cap = cv2.VideoCapture("rtsp://admin:awicam6661@10.15.17.34:554/cam/realmonitor?channel=1&subtype=0") 

count= 0
length = 0
flag = 0
ptime = 0
length1, length2, length3 = 0,0,0
angle1 = 0 
angle2 = 0

while True:
    try:
        success, image = cap.read()
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(imgRGB)
        lmlist1 = []
        lmlist2 = []
        lmlist3 = []

        if results.right_hand_landmarks:
            Hand = results.right_hand_landmarks
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist1.append([id,cx,cy])

        if results.left_hand_landmarks:
            Hand = results.left_hand_landmarks
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist2.append([id,cx,cy])

        if results.pose_landmarks:
            Pose = results.pose_landmarks
            for id,lm in enumerate(Pose.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist3.append([id,cx,cy])


        mpDraw.draw_landmarks(image, results.right_hand_landmarks, mpHolistic.HAND_CONNECTIONS)
        mpDraw.draw_landmarks(image, results.left_hand_landmarks, mpHolistic.HAND_CONNECTIONS)
        mpDraw.draw_landmarks(image, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS, )

        if len(lmlist1) and len(lmlist2):
            x1,y1 = lmlist1[0][1], lmlist1[0][2]
            x2,y2 = lmlist2[0][1], lmlist2[0][2]
            x3,y3 = lmlist3[13][1], lmlist3[13][2] 
            x4,y4 = lmlist3[14][1], lmlist3[14][2]
            x5,y5 = lmlist3[11][1], lmlist3[11][2] 
            x6,y6 = lmlist3[12][1], lmlist3[12][2]
            x7,y7 = lmlist3[15][1], lmlist3[15][2] 
            x8,y8 = lmlist3[16][1], lmlist3[16][2]
            x9,y9 = lmlist3[23][1], lmlist3[23][2]
            x10, y10 = lmlist3[24][1], lmlist3[24][2]
            x11, y11 = lmlist3[25][1], lmlist3[25][2]
            x12, y12 = lmlist3[26][1], lmlist3[26][2]
            x13, y13 = lmlist3[27][1], lmlist3[27][2]
            x14, y14 = lmlist3[28][1], lmlist3[28][2]

            cx,cy = int((x1+x2)//2), int((y1+y2)//2)

            cv2.circle(image, (x1,y1), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x2,y2), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x3,y3), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x4,y4), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x5,y5), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x6,y6), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x7,y7), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x8,y8), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x9,y9), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x10,y10), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x11,y11), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x12,y12), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x13,y13), 10, (0,0,255), cv2.FILLED)
            cv2.circle(image, (x14,y14), 10, (0,0,255), cv2.FILLED)

            shoulder_length = np.sqrt((x6-x5)**2+(y6-y5)**2)
            right_hand_length = np.sqrt((x6-x4)**2+(y6-y4)**2) + np.sqrt((x4-x8)**2+(y4-y8)**2)
            left_hand_length = np.sqrt((x3-x5)**2+(y3-y5)**2) + np.sqrt((x3-x7)**2+(y3-y7)**2)
            length = math.hypot(x2-x1, y2-y1)
            distance = math.hypot(x4-x3, y4-y3)
            knee_distance = math.hypot(x11-x12, y11-y12)
            
            try:
                m1 = (y4-y6)/(x4-x6)
                m2 = (y5-y6)/(x5-x6)
                a1 = np.arctan((m1-m2)/(1+(m1*m2)))
                m3 = (y3-y5)/(x3-x5)
                m4 = (y5-y6)/(x5-x6)
                a2 = np.arctan((m3-m4)/(1+(m3*m4)))
                angle1 = np.rad2deg(abs(a1))
                angle2 = np.rad2deg(abs(a2))
                print("Angle1:",angle1,"Angle2:",angle2)
                print("Knee lenth:",knee_distance)
            except:
                pass
            if(length<shoulder_length and angle1>70.0 and angle2>70.0 and knee_distance>60):
                if flag == 0:
                    flag = 1
                    count+=1

                cv2.line(image, (x5,y5), (x3,y3), (0,255,0), 5)
                cv2.line(image, (x3,y3), (x7,y7), (0,255,0), 5)
                cv2.line(image, (x6,y6), (x4,y4), (0,255,0), 5)
                cv2.line(image, (x4,y4), (x8,y8), (0,255,0), 5)
                cv2.line(image, (x5,y5), (x6,y6), (0,255,0), 5)
                cv2.line(image, (x5,y5), (x9,y9), (0,255,0), 5)
                cv2.line(image, (x6,y6), (x10,y10), (0,255,0), 5)
                cv2.line(image, (x9,y9), (x10,y10), (0,255,0), 5)
                cv2.line(image, (x9,y9), (x11,y11), (0,255,0), 5)
                cv2.line(image, (x10,y10), (x12,y12), (0,255,0), 5)
                cv2.line(image, (x11,y11), (x13,y13), (0,255,0), 5)
                cv2.line(image, (x12,y12), (x14,y14), (0,255,0), 5)


            if (length>shoulder_length and angle1<70.0 and angle2<70.0 and knee_distance<60):
                flag = 0

        cv2.putText(image, f'Count: {int(count)}', (70,150), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.putText(image, f'Length: {int(length)}', (70,100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime

        cv2.putText(image, f'FPS: {int(fps)}', (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.imshow("Image", image)
        K = cv2.waitKey(10)
        if K==ord('q'):
            break
    except:
        continue
cap.release()
cv2.destroyAllWindows()