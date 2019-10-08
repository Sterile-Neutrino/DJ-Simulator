from tkinter import *
from Channel import *
from InfoTable import *

class Component(object):
    def __init__(self, cx, cy, width, height):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        # print(self.__class__.__name__, "width:", self.width)
        # print(self.__class__.__name__, "height:", self.height)
    def act(self):
        pass
    def isClicked(self, x, y):
        return self.cx-self.width//2 <= x <= self.cx+self.width//2 and\
            self.cy-self.height//2 <= y <= self.cy+self.height//2
    def draw(self, canvas):
        canvas.create_rectangle(self.cx-self.width//2, self.cy-self.height//2,
            self.cx+self.width//2, self.cy+self.height//2)
        canvas.create_text(self.cx, self.cy, text=self.__class__.__name__)

class Turntable(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)
        self.image = PhotoImage(file="sources/turntable.gif") 
        self.musicInfo = {}
        self.musicLoc = self.getLoc(self.musicInfo)
        self.channel = Channel(self.cx, self.cy, 
            100, self.musicLoc)

    def getLoc(self, info):
        locs = {}
        for key in info.keys():
            if isinstance(info[key], list):
                locs[key] = info[key]
        return locs

    def act(self):
        self.channel.isDisplayed = True
    
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.image)
        self.channel.draw(canvas)

    def setInfo(self, info):
        self.musicInfo = info
        self.musicLoc = self.getLoc(self.musicInfo)
        self.channel.setInfo(self.musicLoc, self.musicInfo["duration"])
    pass

class Fader(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)
        self.volume = 0.7
        self.image = PhotoImage(file="sources/fader.gif")
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.image)
    pass

class CrossFader(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)
        self.volOne = 0.7
        self.volTwo = 1-self.volOne


class Equalizer(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)
        self.lowVol = 0.7
        self.midVol = 0.7
        self.highVol = 0.7
        self.image = PhotoImage(file="sources/equalizer.gif")
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.image)
    pass

class Effects(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)   

    pass

class Display(Component):
    def __init__(self, cx, cy, width, height):
        super().__init__(cx, cy, width, height)   
        self.image = PhotoImage(file="sources/display.gif")
        self.table = InfoTable() 

    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.image)
        self.table.draw(canvas)

    # def act(self):
    #     self.table.isDisplayed = not self.table.isDisplayed

class Microphone(Component):
    def __init__(self, cx, cy, width=25, height=60):
        super().__init__(cx, cy, width, height)   
        self.image = PhotoImage(file="sources/microphone.gif")

    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.image)

    
