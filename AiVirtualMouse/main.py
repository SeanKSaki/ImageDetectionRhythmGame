import cv2
import math
import random
import time
import keyboard
import tkinter
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


def hit_detection():
    if keyboard.is_pressed('d') and state == 0:
        return True
    elif keyboard.is_pressed('f') and state == 1:
        return True
    elif keyboard.is_pressed('j') and state == 2:
        return True
    elif keyboard.is_pressed('k') and state == 3:
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

def generate_target(_canvas, _window):
    r = 60
    width = _window.winfo_screenwidth()
    height = _window.winfo_screenheight()
    x = random.randint(0, width)
    y = random.randint(0, height)
    return _canvas.create_oval(x-r, y-r, x+r, y+r)

#target = create_random_target()
is_playing = False

window = tkinter.Tk()
window.title("Game Screen")
window.attributes('-fullscreen', True)
c = tkinter.Canvas(window, bg='white', highlightthickness=0)
c.pack(fill=tkinter.BOTH, expand=True)
#target = generate_target(c, window)
first = True
state = 0;
colors = ['red', 'blue', 'green', 'yellow']
while True:
    hit_target = False

    r = 60
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    if first:
        target = c.create_oval(x-r, y-r, x+r, y+r, fill='red')
        first = False



    window.update_idletasks()
    window.update()

    if hit_detection():
        hit_target = True

    if hit_target:
        c.delete(target)
        temp = random.randrange(0, 4)
        if temp == state:
            temp = temp + 1
            if temp == 4:
                temp = 0
        state = temp
        target = c.create_oval(x-r, y-r, x+r, y+r, fill=colors[state])

    #time.sleep(0.05)