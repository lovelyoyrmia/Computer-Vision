'''
import cv2 as cv
import mediapipe as mp
import time


cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands

hands = mpHands.Hands()

mpDraw =  mp.solutions.drawing_utils

pTime = 0

cTime = 0

while True:

    success,frame = cap.read()

    frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):

                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(cx,cy)

                if id == 4:
                    cv.putText(frame,'thumbs',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                elif id == 8: 
                    cv.putText(frame,'index finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                elif id == 12: 
                    cv.putText(frame,'middle finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                elif id == 16: 
                    cv.putText(frame,'ring finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                elif id == 20: 
                    cv.putText(frame,'pinky finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)  

            mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS)

    cTime = time.time()

    fps = 1/(cTime-pTime)

    pTime = cTime

    cv.putText(frame,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow('handtracking',frame)
    key = cv.waitKey(1)

    if key == 81 or key == 113:
        break

'''