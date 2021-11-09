import cv2 as cv
from hand_tracking_module import handDetector

video = cv.VideoCapture(0)

detector = handDetector(maxHands=1)

while True:
    success, frame = video.read()

    if not success:
        break

    frame = detector.findHands(frame)

    # fingers = detector.fingersUp()
    # print(fingers)
    
    cv.imshow('Double hand tracking',frame)

    key = cv.waitKey(1)

    if key == 81 or key == 113:
        break

cv.destroyAllWindows()
video.release()