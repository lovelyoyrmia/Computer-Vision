import cv2 as cv
import mediapipe as mp
import time


class poseDetector():
    def __init__(self,mode=False,modelComplex = 1,smoothnessLM=True,enableSegmentation=False,
                 smoothnessSG=True,detectCon=0.5,trackCon=0.5):
        # self,
        #        static_image_mode=False,
        #        model_complexity=1,
        #        smooth_landmarks=True,
        #        enable_segmentation=False,
        #        smooth_segmentation=True,
        #        min_detection_confidence=0.5,
        #        min_tracking_confidence=0.5,
        self.mode = mode
        self.modelComplex = modelComplex
        self.smoothnessLM = smoothnessLM
        self.enableSegmentation = enableSegmentation
        self.smoothnessSG = smoothnessSG
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelComplex,self.smoothnessLM,
                                     self.enableSegmentation,self.smoothnessSG,
                                     self.detectCon,self.trackCon)

    def findPose(self,frame,draw=True):

        frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        self.results = self.pose.process(frameRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)

        return frame

    def findPosition(self,frame,draw=True):

        lmList = []

        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                # print(cx,cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv.circle(frame,(cx,cy),3,(255,0,255),cv.FILLED)

        return lmList
                    

# def main():
#     video_file = 'files/videos/dance.mp4'

#     video = cv.VideoCapture(video_file)

#     detector = poseDetector()

#     cTime = 0

#     pTime = 0

#     while True:

#         success,frame = video.read()

#         if not success:
#             break

#         detector.findPose(frame)

#         lmList = detector.findPosition(frame)

#         # if len(lmList) !=0 :
#         #     print(lmList[0])
        
#         cTime = time.time()

#         fps = 1/(cTime-pTime)

#         pTime = cTime

#         cv.putText(frame, str(int(fps)),(10,70),cv.FONT_HERSHEY_TRIPLEX,3,(255,0,20),5)

#         cv.imshow('pose tracking',frame)

#         key=cv.waitKey(1)

#         if key == 81 or key == 113:
#             break
    
#     cv.destroyAllWindows()
#     video.release()


# if __name__ == '__main__':
#     main()