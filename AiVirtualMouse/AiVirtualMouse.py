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
cap = cv2.VideoCapture(1)  # 若使用笔记本自带摄像头则编号为0  若使用外接摄像头 则更改为1或其他编号
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
    # 1. 检测手部 得到手指关键点坐标
    img = detector.findHands(img)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (0, 255, 0), 2,  cv2.FONT_HERSHEY_PLAIN)
    lmList = detector.findPosition(img, draw=False)

    # 2. 判断食指和中指是否伸出
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        fingers = detector.fingersUp()

        # 3. 若只有食指伸出 则进入移动模式
        if (fingers[1] == True) and (fingers[0] == False) and (fingers[2] == False) and (fingers[3] == False) and (fingers[4] == False):
            # 4. 坐标转换： 将食指在窗口坐标转换为鼠标在桌面的坐标
            # 鼠标坐标
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

        # 5. 若是食指和中指都伸出 则检测指头距离 距离够短则对应鼠标点击'NoneType' object has no attribute 'Label'
        if (fingers[1] and fingers[2] == True) and (fingers[0] == False) and (fingers[3] == False) and (fingers[4] == False):
            length, img, pointInfo = detector.findDistance(8, 12, img)
            if length < 40:
                cv2.circle(img, (pointInfo[4], pointInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4] == True:
            print("release")
            Keyboard.release('d')
            Keyboard.release('f')
            Keyboard.release('j')
            Keyboard.release('k')

        #Spider-D
        if (fingers[0] and fingers[1] and fingers[4] == True) and (fingers[2] == False) and (fingers[3] == False):
            #autopy.key.tap('d')
            Keyboard.press('d')
            print("Spider - d")

        #Gun-F
        if (fingers[0] and fingers[1] and fingers[2] == True) and (fingers[3] == False) and (fingers[4] == False):
            #autopy.key.tap('f')
            Keyboard.press('f')
            print("Gun - f")

        #Phone-J
        if (fingers[0] and fingers[4] == True) and (fingers[1] == False) and (fingers[2] == False) and (fingers[3] == False):
            #autopy.key.tap('j')
            Keyboard.press('j')
            print("Phone - j")

        #Trident-K
        if (fingers[1] and fingers[2] and fingers[3] == True) and (fingers[4] == False) and (fingers[0] == False):
            #autopy.key.tap('k')
            Keyboard.press('k')

            print("Trident - k")

        if(fingers[2] == True) and (fingers[0] == False) and (fingers[1] == False) and (fingers[3] == False) and (fingers[4] == False):
            Keyboard.press(Key.ctrl)
            Keyboard.press(Key.f4)
            Keyboard.release(Key.ctrl)
            Keyboard.release(Key.f4)
            break;

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps:{int(fps)}', [15, 25],
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)