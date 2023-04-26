import os 
import random
import keyboard
import tkinter
from time import perf_counter

beatmap_path = 'audio/music.beatmap.txt'

def read_beatmap_file(beatmap_path):
    beatmap_path_full = os.path.join(beatmap_path)
    with open(beatmap_path_full, 'rt') as f:
        text = f.read()
    onset_times = [float(string) for string in text.split('\n') if string != '']
    return onset_times

def hit_detection(_target):
    if c.coords(_target)[0] > 40 and c.coords(_target)[0] < 160:
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
        
def generate_target(_canvas, _window):
    r = 60
    width = _window.winfo_screenwidth()
    height = _window.winfo_screenheight()
    #x = random.randint(0, width)
    x = width
    #y = random.randint(0, height)
    y = 540
    return _canvas.create_oval(x-r, y-r, x+r, y+r)

onset_times = read_beatmap_file(beatmap_path)
num_notes = len(onset_times)
random_track_indices = [
        random.randint(0, 3) for _ in range(num_notes)
        ]
active_notes_per_track = {
            track_idx: [] for track_idx in range(3)
            }
onset_hits = {
            onset: False for onset in onset_times
            }

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
c.create_line(100,0,100,1080, fill="green", width=5)
c.create_line(220,0,220,1080, fill="green", width=5)
c.create_line(0, 300, 1920, 300, fill="black", width = 5)
c.create_line(0, 420, 1920, 420, fill="black", width = 5)
c.create_line(0, 540, 1920, 540, fill="black", width = 5)
c.create_line(0, 660, 1920, 660, fill="black", width = 5)
c.create_line(0, 780, 1920, 780, fill="black", width = 5)
    
Text1 = c.create_text(960, 200, text = 'COMBO: 0', fill="black", font=('Helvetica 15 bold'))
combo = 0
i = 0
while True:
        
    hit_target = False
    miss_target = False
    timer = perf_counter()
    current_time = "%.4f" % timer
    #print(current_time)

    r = 60
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    #x = random.randrange(0, width)
    x =  width
    #y = random.randrange(0, height)
    y = 540
    if first:
        target = c.create_oval(x-r, y-r+(3*r), x+r, y+r+(3*r), fill='red')
        first = False

    window.update_idletasks()
    window.update()
    

    c.move(target, -0.4, 0)
    #print(c.coords(target))
    if c.coords(target)[0] <= 0:
        c.delete(Text1)
        combo = 0
        Text1 = c.create_text(960, 200, text = 'MISS!!!!!!', fill="black", font=('Helvetica 15 bold'))
        miss_target = True

    if hit_detection(target):
        c.delete(Text1)
        combo = combo + 1
        string1 = 'COMBO: ' + str(combo)
        Text1 = c.create_text(960, 200, text = string1, fill="black", font=('Helvetica 15 bold'))
        hit_target = True

        
    if hit_target or miss_target:
        c.delete(target) 
        state = random_track_indices[i] 
        i = i + 1
        if state == 0:
            target = c.create_oval(x-r, y-r+(3*r), x+r, y+r+(3*r), fill=colors[state])
        elif state == 1:
            target = c.create_oval(x-r, y-r+(1*r), x+r, y+r+(1*r), fill=colors[state])
        elif state == 2:
            target = c.create_oval(x-r, y-r+(-1*r), x+r, y+r+(-1*r), fill=colors[state])
        elif state == 3:
            target = c.create_oval(x-r, y-r+(-3*r), x+r, y+r+(-3*r), fill=colors[state])
    
    if keyboard.is_pressed('esc'):
        print(onset_times)
        print(random_track_indices)
        break