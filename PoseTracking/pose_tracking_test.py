'''
import cv2 as cv
import mediapipe as mp
import time

video_file = 'files/videos/dance.mp4'

video = cv.VideoCapture(video_file)

mpDraw = mp.solutions.drawing_utils

mpPose = mp.solutions.pose

pose = mpPose.Pose()

cTime = 0

pTime = 0

while True:

    success,frame = video.read()

    if not success:
        break

    frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    results = pose.process(frameRGB)

    print(results.pose_landmarks)

    if results.pose_landmarks:
        for id,lm in enumerate(results.pose_landmarks.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(cx,cy)
                cv.circle(frame,(cx,cy),3,(255,0,255),cv.FILLED)

        mpDraw.draw_landmarks(frame,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
            

    cTime = time.time()

    fps = 1/(cTime-pTime)

    pTime = cTime

    cv.putText(frame, str(int(fps)),(10,70),cv.FONT_HERSHEY_TRIPLEX,3,(255,0,20),5)

    cv.imshow('pose tracking',frame)

    key=cv.waitKey(1)

    if key == 81 or key == 113:
        break

cv.destroyAllWindows()
video.release()
'''