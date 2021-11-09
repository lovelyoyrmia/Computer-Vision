import cv2 as cv
import time
import pose_tracking_module as pose

video_file = 'files/videos/dance.mp4'

video = cv.VideoCapture(video_file)

detector = pose.poseDetector()



cTime = 0

pTime = 0

while True:

    success,frame = video.read()

    if not success:
        break

    frame = detector.findPose(frame)

    lmList = detector.findPosition(frame,draw=False)



    if len(lmList) != 0 :
        print(lmList[0])
        cv.circle(frame, (lmList[14][1], lmList[14][2]),10,(0,0,255),cv.FILLED)
    
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
