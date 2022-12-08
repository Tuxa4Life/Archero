import cv2
from TuxasModule import HandDetector
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(maxHands=2)

isOpen = False
hasAmmo = True

while True: 
    _, img = cap.read()
    img = cv2.flip(img, 1)

    fullList, img = detector.findHands(img, flipType=False)
    if fullList[0] and fullList[1]:
        fireDistance = int(math.hypot(fullList[1][8][0] - fullList[1][4][0], fullList[1][8][1] - fullList[1][4][1]) / 10)
        if fireDistance < 10:
            cv2.line(img, fullList[0][8], fullList[1][8], (0, 255, 0), 2)
            isOpen = False
        else:
            cv2.line(img, fullList[0][8], fullList[1][8], (0, 0, 255), 2)
            isOpen = True

        leftFinger = fullList[0][8]
        rightFinger = fullList[1][8]

        cv2.line(img, (fullList[0][5][0], fullList[0][5][1]), (fullList[0][17][0], fullList[0][17][1]), (0, 0, 128), 10)
        
        angle = int(math.atan2(rightFinger[1] - leftFinger[1], rightFinger[0] - leftFinger[0]) * 100)
        cv2.putText(img, f'Angle: {angle}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

        distance = int(math.hypot(rightFinger[0] - leftFinger[0], rightFinger[1] - leftFinger[1]) / 10)
        cv2.putText(img, f'Power: {distance}', (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

        if hasAmmo:
            cx, cy = (rightFinger[0] + leftFinger[0]) // 2, (rightFinger[1] + leftFinger[1]) // 2
            cv2.line(img, leftFinger, (cx, cy), (0, 0, 100), 5)

        if distance > 20 and hasAmmo and isOpen:
            hasAmmo = False
        elif distance <= 20 and not hasAmmo and not isOpen:
            hasAmmo = True

    cv2.imshow("Bow Game", img)
    cv2.waitKey(1)