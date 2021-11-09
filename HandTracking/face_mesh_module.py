import mediapipe as mp
import cv2 as cv
import time

from mediapipe.python.solutions.drawing_utils import WHITE_COLOR

# drawImg = mpDraw.DrawingSpec(color = GREEN_COLOR)

class faceMesh():
    def __init__(self,mode=False,maxNum=1,detectCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxNum = maxNum
        self.detectCon = detectCon
        self.trackCon = trackCon


        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.face_mesh = self.mpFaceMesh.FaceMesh(self.mode,self.maxNum,self.detectCon,self.trackCon)
        self.draw = self.mpDraw.DrawingSpec(thickness = 1,circle_radius = 1)

    def findFaceMesh(self,frame,draw=True):
        frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        allFaces = []
        self.results = self.face_mesh.process(frameRGB)
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, faceLms, 
                                                self.mpFaceMesh.FACEMESH_CONTOURS,self.draw,self.draw)

                faceMeshList = []

                for id,lm in enumerate(faceLms.landmark):
                    h,w,c = frame.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    cv.putText(frame,str(id),(cx,cy),cv.FONT_HERSHEY_PLAIN,0.3,WHITE_COLOR,1)
                    faceMeshList.append([id,cx,cy])
            allFaces.append(faceMeshList)

        return frame,allFaces
    

def main():
    video = cv.VideoCapture(0)
    cTime = 0
    pTime = 0

    detector = faceMesh()
    while True:
        success,frame = video.read()
        if not success:
            break
        frame,allFaces = detector.findFaceMesh(frame)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(frame,f'fps: {int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(255,255,0),2)
        cv.imshow('face mesh',frame)
        key = cv.waitKey(1)

        if key == 81 or key == 113:
            break

    cv.destroyAllWindows()
    video.release()

    

if __name__ == '__main__':
    main()