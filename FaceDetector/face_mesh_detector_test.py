import mediapipe as mp
import cv2 as cv
import time

from mediapipe.python.solutions.drawing_utils import GREEN_COLOR

video = cv.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
face_mesh = mpFaceMesh.FaceMesh()
draw = mpDraw.DrawingSpec(thickness = 1,circle_radius = 1)
# drawImg = mpDraw.DrawingSpec(color = GREEN_COLOR)

cTime = 0
pTime = 0

while True:
    success,frame = video.read()

    if not success:
        break

    frameRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    results = face_mesh.process(frameRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            for id,lm in enumerate(faceLms.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
            mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS,draw)

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
