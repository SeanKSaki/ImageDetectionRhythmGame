import cv2
import mediapipe as mp 
from playsound import playsound
from timer import Timer
from scoreboard import Scoreboard
from schedulers import *

wCam, hCam = 720, 540

rectangle_frames = 0
rectangle_coords = (200,200)

scoreboard = Scoreboard(0, 1)

def detect_hit(landmark,rectangle_coords1,rectangle_coords2,size=(wCam,hCam)):
  normalized_x1 = rectangle_coords1[0]/size[0]
  normalized_y1 = rectangle_coords1[1]/size[1]
  normalized_x2 = rectangle_coords2[0]/size[0]
  normalized_y2 = rectangle_coords2[1]/size[1]
  return normalized_x1 < landmark[7].x < normalized_x2 and normalized_y1 < landmark[7].y < normalized_y2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()
mpDrawStyles = mp.solutions.drawing_styles

currentHitObject = 0
timer = Timer()
timer.start()

name = 'sasageyo'

playsound('./songs/' + name + '.mp3', block=False)

pressed = False

hittable_stack = []
scheduler = OsuScheduler("./songs/" + name+ ".txt",size=(wCam,hCam))

while True:
    success, img = cap.read()
    img = cv2.resize(img, (wCam,hCam), interpolation =cv2.INTER_AREA)
    t = timer.getTime()
    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while scheduler.next_time() < t:
      hold = next(scheduler)
      if hold == None:
        break
      hittable_stack.append(hold)
    i = 0
    for i in range(len(hittable_stack)):
      if hittable_stack[i] and hittable_stack[i].time_tup[1] >= t:
        break
    if i != 0:
      print('miss')
      scoreboard.resetMultiplier()
    hittable_stack = hittable_stack[i:]
    for item in hittable_stack:
      if item == None:
        break
      img = item.apply(img,t)
      
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    
    img = cv2.flip(img, 1)
    img = cv2.putText(img, str(scoreboard.getScore()), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
    img = cv2.putText(img, str(scoreboard.getMultiplier()) + "x", (560, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
    img = cv2.flip(img, 1)
    handsFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    if results.multi_hand_landmarks:
                for handLMS in results.multi_hand_landmarks:
                    lmList = []
                    for id, lm in enumerate(handLMS.landmark):
                        h, w, c = handsFrame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    indexX = 0
                    indexY = 0
                    indexMid = 0
                    handBottomX = 0
                    handBottomY = 0
                    pinkyX = 0
                    pinkyY = 0
                    fistWarning = "Fist!"
                    for lms in lmList:
                        if lms[0] == 7:
                            indexX, indexY = lms[1], lms[2]
                        elif lms[0] == 5:
                            indexMid = lms[2]
                        elif lms[0] == 19:
                            pinkyX, pinkyY = lms[1], lms[2]
                        elif lms[0] == 0:
                            handBottomX, handBottomY = lms[1], lms[2]
                    if (indexY < handBottomY) and (indexY > indexMid):
                        cv2.rectangle(handsFrame, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                        cv2.putText(handsFrame, fistWarning, (pinkyX + 2, indexY - 2), (font), .7,
                                    (0, 0, 255), 1, cv2.LINE_4)
                        pressed = True
    
    
    if len(hittable_stack):
      try:
        if not hittable_stack:
          break
        rectangle_coords =   hittable_stack[0].location_tup
        rectangle_coords2 = (rectangle_coords[0]-100,rectangle_coords[1]-100)
        
        if results.multi_hand_landmarks:
          for lands in results.multi_hand_landmarks:
            hit = detect_hit(lands.landmark,rectangle_coords2,rectangle_coords)
            if pressed and hit and hittable_stack[0].hittable:
              print("hit") 
              hittable_stack.pop(0)
              scoreboard.addScore(100)
              scoreboard.setMultiplier(scoreboard.getMultiplier() + 1)
              break
      
      except Exception as e:
        print(e)
        break
                                              
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mpDraw.draw_landmarks(
            img,
            hand_landmarks,
            mpHands.HAND_CONNECTIONS,
            mpDrawStyles.get_default_hand_landmarks_style(),
            mpDrawStyles.get_default_hand_connections_style())

    pressed = False 

    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Image", cv2.flip(img, 1))
    if cv2.waitKey(32) == 32:
      print('Pressed space')
      pressed = True
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()