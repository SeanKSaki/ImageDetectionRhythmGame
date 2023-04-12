import cv2
import math
import random
import time
from cvzone.HandTrackingModule import HandDetector

wCam, hCam = 1280, 720
frameR = 144
smoothening = 1
target_radius = 40
hand_radius = 40  
border_size = 15 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)  
detector = HandDetector(detectionCon=0.8, maxHands=2)

class Circle:

    def __init__(self, coordinates, radius, color, thickness):
        self.coordinates = coordinates
        self.radius = radius
        self.color = color
        self.thickness = thickness

    def draw(self, _frame):
        cv2.circle(_frame, self.coordinates, self.radius, self.color, self.thickness)

    def check_intersection(self, other_coordinates, other_radius):
        distance = math.sqrt(math.pow(other_coordinates[0] - self.coordinates[0], 2) + math.pow(
            other_coordinates[1] - self.coordinates[1], 2))

        if distance <= self.radius + other_radius:
            return True
        else:
            return False


def create_random_target(current_target_pos=[]):
    if current_target_pos:
        possible_x = []

        x_limit = [target_radius + border_size + 15, wCam - target_radius - border_size - 15]
        y_limit = [target_radius + border_size + 15, hCam - target_radius - border_size - 15]

        for i in range(x_limit[0], x_limit[1]):
            if i + 100 < current_target_pos[0] or i - 100 > current_target_pos[0]:
                possible_x.append(i)

        possible_y = []
        for i in range(y_limit[0], y_limit[1]):
            if i + 100 < current_target_pos[1] or i - 100 > current_target_pos[1]:
                possible_y.append(i)

        if not possible_x:
            possible_x = range(x_limit[0], x_limit[1])

        if not possible_y:
            possible_y = range(y_limit[0], y_limit[1])

    else:
        possible_x = range(target_radius + border_size, wCam - target_radius - border_size)
        possible_y = range(target_radius + border_size, hCam - target_radius - border_size)

    random_x = random.choice(possible_x)
    random_y = random.choice(possible_y)
    random_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 256)]
    _target = Circle([random_x, random_y], target_radius, random_color, -1)

    return _target


target = create_random_target()
is_playing = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT,
                               value=[0, 0, 0])

    hit_target = False
    hands = detector.findHands(img, flipType=False, draw=False)
    target.draw(img)

    if hands:
        for i in range(len(hands)):
            hand_position = hands[i]["center"]
            hand_circle = Circle(hand_position, hand_radius, (0, 0, 255), 1)

            if target.check_intersection(hand_circle.coordinates, hand_circle.radius):
                hand_circle.color = (0,255,0)
                hit_target = True
            else:
                hand_circle.color = (0,0,255)
            hand_circle.draw(img)
    if hit_target:
        target = create_random_target(target.coordinates)

    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.imshow("Image", img)
    cv2.waitKey(1)