try: 
    import mediapipe as mp
    import cv2 as cv
    import time
    import sys
except Exception as e:
    print('Modules are missing {}'.format(e))

class faceDetector():
    def __init__(self, detectionCon = 0.5,modelSelect = 0) :
        self.detectionCon = detectionCon
        self.modelSelect = modelSelect

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceDetection = mp.solutions.face_detection
        self.face_detection = self.mpFaceDetection.FaceDetection(self.detectionCon,self.modelSelect)

    def findFace(self,frame,draw = True):

        frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        self.results = self.face_detection.process(frameRGB)

        boundingBoxList = []

        if self.results.detections: 
            
            for id,detection in enumerate(self.results.detections):

                boundingBoxC = detection.location_data.relative_bounding_box
                fh, fw, fc = frame.shape
                boundingBox = int(boundingBoxC.xmin * fw), int(boundingBoxC.ymin * fh), \
                                int(boundingBoxC.width * fw), int(boundingBoxC.height * fh)
                boundingBoxList.append([id,boundingBox,detection.score])

                if draw:
                    frame = self.fancyDraw(frame,boundingBox)
                    cv.putText(frame,f'{int(detection.score[0]*100)}%',(boundingBox[0],boundingBox[1]-28),
                                cv.FONT_HERSHEY_PLAIN,2,(0,255,0),3)

        return frame, boundingBoxList

    def fancyDraw(self,frame,boundingBox,l=30,t=5,rt=1):
        x,y,w,h = boundingBox
        x1,y1 = x+w,y+h

        cv.rectangle(frame,boundingBox,(255,0,255),rt)
        # Top Left Corner drawing
        cv.line(frame,(x,y),(x+l,y),(0,255,0),t)
        cv.line(frame,(x,y),(x,y+l),(0,255,0),t)

        # Bottom Left Corner drawing
        cv.line(frame,(x,y1),(x+l,y1),(0,255,0),t)
        cv.line(frame,(x,y1),(x,y1-l),(0,255,0),t)

        # Top Right Corner drawing
        cv.line(frame,(x1,y),(x1-l,y),(0,255,0),t)
        cv.line(frame,(x1,y),(x1,y+l),(0,255,0),t)

        # Bottom Right Corner drawing
        cv.line(frame,(x1,y1),(x1-l,y1),(0,255,0),t)
        cv.line(frame,(x1,y1),(x1,y1-l),(0,255,0),t)

        return frame



def main():

    video = cv.VideoCapture(0)

    detector = faceDetector()

    cTime = 0

    pTime = 0

    while True:
        success,frame = video.read()
  
        if not success:
            break

        detectList = detector.findFace(frame)

        if len(detectList) != 0:
            print(detectList[0])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame,f'fps : {int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
        
        cv.imshow('face detector',frame)
        key=cv.waitKey(1)
        if key==81 or key==113:
            break

    cv.destroyAllWindows()
    video.release()


if __name__ == '__main__':
    main()
