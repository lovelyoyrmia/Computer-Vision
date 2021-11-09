import cv2 as cv
import mediapipe as mp
import math

class handDetector():
    def __init__(self,mode = False,maxHands = 2,detectionCon = 0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                        self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipId = [4,8,12,16,20]
        # self.lmList = []
        
    def findHands(self,frame,draw = True,):
        
        frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        self.results = self.hands.process(frameRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
                    self.findPosition(frame)
                    self.fingersUp(frame)

        return frame

    def findPosition(self,frame,handNumber = 0,draw = True):
        xList = []
        yList = []
        boundingBox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]

            for id,lm in enumerate(myHand.landmark):

                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                xList.append(cx)
                yList.append(cy)

                self.lmList.append([id,cx,cy])
                # if draw:
                #     if id == 4:
                #         cv.putText(frame,'thumb',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                #     elif id == 8: 
                #         cv.putText(frame,'index finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                #     elif id == 12: 
                #         cv.putText(frame,'middle finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                #     elif id == 16: 
                #         cv.putText(frame,'ring finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
                #     elif id == 20: 
                #         cv.putText(frame,'pinky finger',(cx-30,cy-20),cv.FONT_HERSHEY_PLAIN,1,(255,255,0),2) 
            xMin,xMax = min(xList),max(xList)
            yMin,yMax = min(yList),max(yList)
            boundingBox = xMin,yMin,xMax,yMax

            if draw:
                for i in self.lmList:
                    cv.rectangle(frame,(boundingBox[0]-20,boundingBox[1]-20),
                                (boundingBox[2]+20,boundingBox[3]+20),(255,255,0),2)
                    # print(i)


        return self.lmList,boundingBox

    def fingersUp(self,frame):
        fingers = []
        if self.lmList[self.tipId[0]][1] > self.lmList[self.tipId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if self.lmList[self.tipId[id]][2] < self.lmList[self.tipId[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers = fingers.count(1)
        print(totalFingers)
        cv.rectangle(frame,(20,275),(150,425),(255,0,0),cv.FILLED)
        cv.putText(frame,str(totalFingers),(60,375),cv.FONT_HERSHEY_PLAIN,5,(255,255,255),6)
        return fingers

    def findDistance(self,frame,p1,p2,draw = True):
        '''variable to get positions of index finger and thumb'''
        x1,y1 = self.lmList[p1][1],self.lmList[p1][2]
        x2,y2 = self.lmList[p2][1],self.lmList[p2][2]

        '''variable center circle'''
        cx,cy = (x1+x2)//2,(y1+y2)//2

        if draw:
            '''draw circle on finger'''
            cv.circle(frame,(x1,y1),10,(0,255,0),cv.FILLED)
            cv.circle(frame,(x2,y2),10,(0,255,0),cv.FILLED)
            cv.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv.circle(frame,(cx,cy),10,(0,255,0),cv.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        return length,frame,[x1,y1,x2,y2,cx,cy]
