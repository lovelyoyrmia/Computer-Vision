import cv2 as cv
import time
import hand_tracking_module as hd
import face_mesh_module as fd
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

'''Initialization Audio devices controller'''
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

'''Declare varible volume which you will use'''
volRange = volume.GetVolumeRange()
cVol = volume.GetMasterVolumeLevel()
volume.SetMasterVolumeLevel(cVol,None)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPercent = 0

'''Declare variable to get video capture,hand detector,and face mesh'''
cap = cv.VideoCapture(0)
cTime = 0
pTime = 0
area = 0
detector = hd.handDetector(detectionCon=0.7)
detectFace = fd.faceMesh()


while True:

	success,frame = cap.read()

	if not success:
		break

	# frame,allFaces = detectFace.findFaceMesh(frame)

	frame = detector.findHands(frame)
	
	# if draw = False then the text of family fingers are not visible

	lmList, boundingBox = detector.findPosition(frame)

	# fingers = detector.fingersUp()
	if len(lmList) !=0 :

		area = (boundingBox[2]-boundingBox[0]) * (boundingBox[3]-boundingBox[1])//100

		if 250 < area < 1000:

			'''variable to get positions of index finger and thumb'''
			x1,y1 = lmList[4][1],lmList[4][2]
			x2,y2 = lmList[8][1],lmList[8][2]

			'''variable center circle'''
			cx,cy = (x1+x2)//2,(y1+y2)//2

			'''draw circle on finger'''
			cv.circle(frame,(x1,y1),10,(0,255,0),cv.FILLED)
			cv.circle(frame,(x2,y2),10,(0,255,0),cv.FILLED)
			cv.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
			cv.circle(frame,(cx,cy),10,(0,255,0),cv.FILLED)

			length = math.hypot(x2-x1,y2-y1)

			if length < 50:
				cv.circle(frame,(cx,cy),10,(0,0,255),cv.FILLED)

			vol = np.interp(length,[30,280],[minVol,maxVol])
			volBar = np.interp(length,[30,280],[400,150])
			volPercent = np.interp(length,[30,280],[0,100])
			print(int(length),vol)
			volume.SetMasterVolumeLevel(vol,None)

	cv.rectangle(frame,(50,150),(85,400),(0,255,0),3)
	cv.rectangle(frame,(50,int(volBar)),(85,400),(0,255,0),cv.FILLED)
	cv.putText(frame,f'{int(volPercent)} %',(30,450),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
	

	cTime = time.time()

	fps = 1/(cTime-pTime)

	pTime = cTime

	cv.putText(frame,f'fps: {int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(255,255,0),2)

	cv.imshow('handtracking',frame)
	key = cv.waitKey(1)

	if key == 81 or key == 113:
		break

cv.destroyAllWindows()

cap.release()
