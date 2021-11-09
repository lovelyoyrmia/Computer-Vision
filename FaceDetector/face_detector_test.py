import mediapipe as mp
import cv2 as cv
import time

video = cv.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils

mpFaceDetection = mp.solutions.face_detection

face_detection = mpFaceDetection.FaceDetection()

cTime = 0

pTime = 0

while True:
    success,frame = video.read()

    if not success:
        break

    frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    results = face_detection.process(frameRGB)

    
    if results.detections:
        for id,detection in enumerate(results.detections):
            # print(detection)
            # mpDraw.draw_detection(frame,detection)
            boundingBoxC = detection.location_data.relative_bounding_box
            fh, fw, fc = frame.shape
            boundingBox = int(boundingBoxC.xmin * fw), int(boundingBoxC.ymin * fh), \
                          int(boundingBoxC.width * fw), int(boundingBoxC.height * fh)

            cv.rectangle(frame,boundingBox,(255,0,255),3)
            cv.putText(frame,f'{int(detection.score[0]*100)}%',(boundingBox[0],boundingBox[1]-28),
                        cv.FONT_HERSHEY_PLAIN,2,(0,255,0),3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(frame,f'fps : {int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
    
    cv.imshow('face detector',frame)
    key=cv.waitKey(1)
    if key==81 or key==113:
        break

cv.destroyAllWindows()
video.release()