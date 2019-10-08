from tkinter import *
import time
from pygame import mixer


def play_music(data):   
    mixer.music.play()
    # mixer.music.queue("music/Claes.mp3")

def pause_music(data):
    print(mixer.music.get_busy())
    if data.paused == False:
        mixer.music.pause()
        data.paused = True
    else:
        mixer.music.unpause()
        data.paused = False

def stop_music():
    # mixer.music.rewind()
    mixer.music.stop()
    # time.sleep(0.5)
    mixer.music.load("music/Lynx.ogg")
    mixer.music.play(1,100)
    print(mixer.music.get_busy())




class Button(object):
    def __init__(self, cx, cy):
        self.r = 30
        self.cx = cx
        self.cy = cy

    def isClicked(self, x, y):
        return ((x-self.cx)**2+(y-self.cy)**2)**0.5 <= self.r

    def act(self, data):
        pass

    def draw(self, canvas):
        # draw the block of the button
        canvas.create_oval(self.cx-self.r, self.cy-self.r, 
            self.cx+self.r, self.cy+self.r)
        canvas.create_text(self.cx, self.cy, 
            text=self.__class__.__name__, font="Arial 14")

class Start(Button):
    def act(self, data):
        play_music(data)

class Pause(Button):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.paused = False

    def act(self, data):
        pause_music(data)
        self.paused = data.paused

    def draw(self, canvas):
        # draw the block of the button
        canvas.create_oval(self.cx-self.r, self.cy-self.r, 
            self.cx+self.r, self.cy+self.r, 
            fill = "red" if self.paused else "green")
        canvas.create_text(self.cx, self.cy, 
            text=self.__class__.__name__, font="Arial 14", fill="white")

class Stop(Button):
    def act(self, data):
        stop_music()

class volUp(Button): 
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.r //= 2

    def act(self, data):
        if data.volume <= 1:
            data.volume += 0.1
        mixer.music.set_volume(data.volume)

    def draw(self, canvas):
        # draw the block of the button
        canvas.create_oval(self.cx-self.r, self.cy-self.r, 
            self.cx+self.r, self.cy+self.r, activefill = "green")
        canvas.create_text(self.cx, self.cy, 
            text="+", font="Arial 18")

class volDown(Button): 
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.r //= 2

    def act(self, data):
        if data.volume >= 0:
            data.volume -= 0.1
        mixer.music.set_volume(data.volume)

    def draw(self, canvas):
        # draw the block of the button
        canvas.create_oval(self.cx-self.r, self.cy-self.r, 
            self.cx+self.r, self.cy+self.r, activefill = "green")
        canvas.create_text(self.cx, self.cy, 
            text="-", font="Arial 18")



# Animation Starter Code, Focus on timerFired

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    mixer.init()
    mixer.music.load("music/Bonzo's Juggling Show.ogg")
    data.buttons = []
    initializeButtons(data)
    data.paused = False
    data.volume = 0.7
    mixer.music.set_volume(data.volume)
    pass

def initializeButtons(data):
    data.buttons.append(Start(data.width//5, data.height//2))
    data.buttons.append(Pause(data.width*2//5, data.height//2))
    data.buttons.append(Stop(data.width*3//5, data.height//2))
    data.buttons.append(volUp(data.width*4//5, data.height//3))
    data.buttons.append(volDown(data.width*4//5, data.height*2//3))

def mousePressed(event, data):
    # use event.x and event.y
    for b in data.buttons:
        if b.isClicked(event.x, event.y):
            b.act(data)
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    for b in data.buttons:
        b.draw(canvas)

    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)