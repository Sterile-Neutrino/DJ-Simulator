# Animation Starter Code, Focus on timerFired

from tkinter import *

####################################
# customize these functions
####################################

class Channel(object):
    def __init__(self, x, y, t, musicLoc):
        self.x = x
        self.y = y
        self.width = 750
        self.height = 15
        self.start = self.x-self.width//2
        self.time = t 
        self.block = Block(self.x-self.width/2, self.y)
        self.speed = self.width / self.time
        self.cue = []
        self.musicLoc = musicLoc
        self.musicColor = {"intro":"blue", "verse":"cyan",
            "buildup":"orange", "break":"yellow",
            "drop":"red", "outro":"green"}
        self.initializeCue(self.y)
        self.cued = False
        self.isPlayed = False
        self.isDisplayed = False

    def setCx(self, x):
        self.x = x
        self.block.x = x-self.width/2
        self.start = self.x-self.width//2
    
    def setCy(self, y):
        self.y = y
        self.block.y = y
        self.initializeCue(self.y)

    def setInfo(self, info, duration):
        self.musicLoc = info
        self.block.x = self.start
        self.time = duration
        self.speed = self.width / self.time
        self.initializeCue(self.y)

    def initializeCue(self, y):
        self.cue = []
        lastPoint = 0
        for locs in self.musicLoc:
            for loc in self.musicLoc[locs]:
                startPoint = loc[0]
                lastPoint = loc[1]
                newCue = Cue(self.start+self.speed*startPoint, y-self.height/2)
                if newCue not in self.cue:
                    self.cue.append(newCue)
        self.cue.append(Cue(self.start+self.speed*lastPoint, y-self.height/2))

    def moveBlock(self):
        self.block.x += self.speed

    def draw(self, canvas):
        if self.isDisplayed:
            for locs in self.musicLoc:
                for loc in self.musicLoc[locs]:
                    startPoint = loc[0]
                    endPoint = loc[1]
                    startPos = self.start+self.width*(startPoint/self.time)
                    endPos = self.start+self.width*(endPoint/self.time)
                    canvas.create_rectangle(startPos, self.y-self.height/2, 
                        endPos, self.y+self.height/2, fill=self.musicColor[locs])
            for cue in self.cue:
                cue.draw(canvas)
            self.block.draw(canvas)



class Block(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20

    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width//2, self.y-self.height//2, 
            self.x+self.width//2, self.y+self.height//2, fill="yellow")

class Cue(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.color = "red"
        self.cued = False
        self.isDisplayed = False

    def isClicked(self, x, y):
        return self.x-self.width//2 <= x <= self.x+self.width//2 and \
            self.y-self.height <= y <= self.y

    def draw(self, canvas):
        canvas.create_polygon(self.x-self.width//2, self.y-self.height,
            self.x+self.width//2, self.y-self.height, self.x, self.y, fill=self.color)
