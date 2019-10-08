# Animation Starter Code, Focus on timerFired

from tkinter import *
import random
from Performance import *
from Studio import *

class Button(object):
    def __init__(self, cx, cy, text="Button"):
        self.w = 300
        self.h = 80
        self.x = cx
        self.y = cy
        self.text=text

    def isClicked(self, x, y):
        return self.x-self.w//2 <= x <= self.x+self.w//2 and\
            self.y-self.h//2 <= y <= self.y+self.h//2

    def act(self, data):
        pass

    def draw(self, canvas, color):
        # draw the block of the button
        canvas.create_rectangle(self.x-self.w//2, self.y-self.h//2, self.x+self.w//2, self.y+self.h//2, width=5)
        canvas.create_text(self.x, self.y, 
            text=self.__class__.__name__, font="Impact 50 bold", fill=color)

class StartCareer(Button):
    def __init__(self, cx, cy, text="Start new Career"):
        super().__init__(cx, cy, text)

    def act(self, data):
        data.gameState = "studio"
        initializeStudio(data)

class StartPerforme(Button):
    def __init__(self, cx, cy, text="Start new mix"):
        super().__init__(cx, cy, text)

    def act(self, data):
        data.gameState = "performance"
        initializePerformance(data)

class Quit(Button):
    def __init__(self, cx, cy, text="Quit"):
        super().__init__(cx, cy, text)

    def act(self, data):
        root.destroy()

####################################
# customize these functions
####################################

def initializeMainManu(data):
    # load data.xyz as appropriate
    data.images = [PhotoImage(file="sources/turntable.gif"), PhotoImage(file="sources/display.gif"), 
        PhotoImage(file="sources/equalizer.gif"), PhotoImage(file="sources/microphone.gif"), PhotoImage(file="sources/fader.gif")]
    data.currImage = [[random.choice(data.images), random.randint(0,1000), -50, False]]
    data.titleColor = ["red", "blue", "green", "yellow", "orange", "purple", "grey", "black"]
    data.color = random.choice(data.titleColor)
    data.timer = 0
    data.showLoadSaves = False
    data.startCareer = StartCareer(data.width//2, data.height//2)
    data.StartPerforme = StartPerforme(data.width//2, data.height//2+150)
    data.quit = Quit(data.width//2, data.height//2+300)
    data.buttons = [data.startCareer, data.StartPerforme, data.quit]
    pass

def mousePressedMainManu(event, data):
    # use event.x and event.y
    for button in data.buttons:
        if button.isClicked(event.x, event.y):
            button.act(data)
    pass

def keyPressedMainManu(event, data):
    # use event.char and event.keysym
    pass

def timerFiredMainManu(data):
    for img in data.currImage:
        x = img[1]
        y = img[2]
        if y > 150 and img[3] == False:
            data.currImage.append([random.choice(data.images), random.randint(0,1000), -100, False])
            img[3] = True
        if y > 1000:
            data.currImage.remove(img)
        img[2] += 5
    if data.timer % 10 == 0:
        data.color = random.choice(data.titleColor)
    data.timer += 1
    
    pass

def redrawAllMainManu(canvas, data):
    # draw in canvas
    for img in data.currImage:
        canvas.create_image(img[1], img[2], image=img[0])
    canvas.create_text(data.width//2, data.height//3, text="D J    S I M U L A T O R", font="Impact 90 bold", fill=data.color)
    for button in data.buttons:
        button.draw(canvas, data.color)
    pass

