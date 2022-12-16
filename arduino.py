import cv2
import TuxasModule
import math 
from cvzone.SerialModule import SerialObject

cap = cv2.VideoCapture(0)
detector = TuxasModule.HandDetector(maxHands=2, detectionCon=.8)
arduino = SerialObject()

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    list, img = detector.findHands(img)

    if list[0] and list[1]:
        cv2.line(img, list[0][8], list[1][8], (255, 255, 255), 2)

        angle = int(math.degrees(math.atan2(list[1][8][1] - list[0][8][1], list[1][8][0] - list[0][8][0])))
        angle = abs(angle)

        cv2.putText(img, f'Angle: {angle}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        if len(str(angle)) == 1:
            arduino.sendData([f'00{angle}'])
        elif len(str(angle)) == 2:
            arduino.sendData([f'0{angle}'])
        else: 
            arduino.sendData([angle])

    cv2.imshow('Window', img)
    cv2.waitKey(1)