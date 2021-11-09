import cv2 as cv
import time
import hand_tracking_module as hd
import face_mesh_module as fd
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
video = cv.VideoCapture(0)
cTime = 0
pTime = 0
area = 0
detector = hd.handDetector(detectionCon=0.7,maxHands=1)
detectFace = fd.faceMesh()
colorVol = (255,255,0)

while True:

	success,frame = video.read()

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
			'''Find distance between index and thumb'''
			length,frame,lineInfo = detector.findDistance(frame,4,8)

			'''Convert volume'''
			volBar = np.interp(length,[30,280],[400,150])
			volPercent = np.interp(length,[30,280],[0,100])
			
			'''Reduce to make it smoother'''
			smoothness = 10
			volPercent = smoothness * round(volPercent/smoothness)

			'''Check  fingers up'''
			fingers = detector.fingersUp()
			if not fingers[4]:
				volume.SetMasterVolumeLevelScalar(volPercent/100,None)
				cv.circle(frame,(lineInfo[4],lineInfo[5]),10,(0,0,255),cv.FILLED)
				colorVol = (0,0,255)
			else:
				colorVol = (255,255,0)

	cv.rectangle(frame,(50,150),(85,400),(0,255,0),3)
	cv.rectangle(frame,(50,int(volBar)),(85,400),(0,255,0),cv.FILLED)
	cVolScalar = int(volume.GetMasterVolumeLevelScalar()*100)
	cv.putText(frame,f'Set Volume: {int(cVolScalar)} %',(300,70),cv.FONT_HERSHEY_PLAIN,2,colorVol,2)
	cv.putText(frame,f'{int(volPercent)} %',(30,450),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
	
	cTime = time.time()

	fps = 1/(cTime-pTime)

	pTime = cTime

	cv.putText(frame,f'fps: {int(fps)}',(10,70),cv.FONT_HERSHEY_PLAIN,2,(255,255,0),2)

	cv.imshow('hand tracking',frame)
	key = cv.waitKey(1)

	if key == 81 or key == 113:
		break

cv.destroyAllWindows()

video.release()
