import cv2
import HandTrackingModule as htm
import autopy
import numpy as np
import time
import cvzone
import pynput
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

##############################
wCam, hCam = 1280, 720
frameR = 144
smoothening = 1
##############################
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector()
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

Keyboard = KeyboardController()
Mouse = MouseController()

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 255, 0), 2,  cv2.FONT_HERSHEY_PLAIN)
    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] ## index
        fx1, fy1 = lmList[4][1:] ## thumb
        fx3, fy3 = lmList[12][1:] ## middle
        fx4, fy4 = lmList[16][1:]  ## ring
        fx5, fy5 = lmList[20][1:]  ## pinky
        fingers = detector.fingersUp()

        ## only index finger up
        if (fingers[1] == True) and (fingers[0] == False) and (fingers[2] == False) and (fingers[3] == False) and (fingers[4] == False):


            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            print(x3, y3)
            # smoothening values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            if (0 < wScr - clocX < 1920) and (0 < clocY < 1080):
                print(wScr - clocX, clocY)
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

        ## both index and thumb
        if (fingers[1] and fingers[0] == True) and (fingers[2] == False) and (fingers[3] == False) and (fingers[4] == False):
            length, img, pointInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (pointInfo[4], pointInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        ## key releasing with all fingers up
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4] == True:
            print("release")
            Keyboard.release('d')
            Keyboard.release('f')
            Keyboard.release('j')
            Keyboard.release('k')

        # Spider-D
        if (fingers[0] and fingers[1] and fingers[4] == True) and (fingers[2] == False) and (fingers[3] == False):
            length, img, pointInfo = detector.findDistance(8, 12, img)
            #autopy.key.tap('d')
            Keyboard.press('d')
            print("Spider - d")
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        # Gun-F
        if (fingers[0] and fingers[1] and fingers[2] == True) and (fingers[3] == False) and (fingers[4] == False):
            #autopy.key.tap('f')
            Keyboard.press('f')
            print("Gun - f")
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        # Phone-J
        if (fingers[0] and fingers[4] == True) and (fingers[1] == False) and (fingers[2] == False) and (fingers[3] == False):
            #autopy.key.tap('j')
            Keyboard.press('j')
            print("Phone - j")
            cv2.circle(img, (fx1, fy1), 15, (255, 0, 255), cv2.FILLED)

        # Trident-K
        if (fingers[1] and fingers[2] and fingers[3] == True) and (fingers[4] == False) and (fingers[0] == False):
            #autopy.key.tap('k')
            Keyboard.press('k')
            print("Trident - k")
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        if(fingers[2] == True) and (fingers[0] == False) and (fingers[1] == False) and (fingers[3] == False) and (fingers[4] == False):
            Keyboard.press(Key.ctrl)
            Keyboard.press(Key.f4)
            Keyboard.release(Key.ctrl)
            Keyboard.release(Key.f4)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            break;

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps:{int(fps)}', [15, 25],
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)