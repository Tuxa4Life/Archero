import cv2
import TuxasModule

cap = cv2.VideoCapture(0)
detector = TuxasModule.HandDetector(detectionCon=.7)

lineCords = []
cx = 320
cy = 240

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    lms, img = detector.findHands(img)
    if lms[1]:
        cv2.circle(img, lms[1][8], 7, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (cx, cy), lms[1][8], (255, 255, 255), 3)

    cv2.imshow('Testing', img)
    cv2.waitKey(1)