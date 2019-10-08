# Animation Starter Code, Focus on timerFired
from pygame import mixer
import math
from tkinter import *
from Component import *
from People import *
from MainManu import *
from Performance import *
from Studio import *
import os

class Controller(object): 
    def __init__(self, cx, cy, width, height):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.turntable1 = Turntable(self.cx-self.width//4-20,
            self.cy+25, self.width//3, self.height*3//5+16)
        # self.turntable1.channel.isPlayed = True
        self.turntable1.channel.setCx(500)
        self.turntable1.channel.setCy(45)
        self.turntable2 = Turntable(self.cx+self.width//4+20,
            self.cy+25, self.width//3, self.height*3//5+16)
        self.turntable2.channel.setCx(500)
        self.turntable2.channel.setCy(90)
        self.equalizer = Equalizer(self.cx, self.cy*15//16-15,
            self.width//5, self.height//2)
        self.fader1 = Fader(self.cx-self.width//20, self.cy*23//21,
            self.width//10, self.height//3)
        self.fader2 = Fader(self.cx+self.width//20, self.cy*23//21,
            self.width//10, self.height//3)
        self.display1 = Display(self.cx-self.width//4-20,
            self.cy-90, self.width//3, self.height//4)
        self.display2 = Display(self.cx+self.width//4+20,
            self.cy-90, self.width//3, self.height//4)
        self.microphone = Microphone(self.cx+self.width//4+200, self.cy)
        self.component = [self.turntable1, self.turntable2, self.equalizer,
            self.fader1, self.fader2, self.display1, self.display2, self.microphone]

    def draw(self, canvas):
        canvas.create_rectangle(self.cx-self.width//2, self.cy-self.height//2,
            self.cx+self.width//2, self.cy+self.height//2, fill="grey15")
        canvas.create_rectangle(self.cx-self.width//2+10, self.cy-self.height//2+10,
            self.cx+self.width//2-10, self.cy+self.height//2-10, width=5, outline="firebrick4")   
        for component in self.component:
            component.draw(canvas)

class Setting(object):
    def __init__(self, cx, cy, width, height):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height

    def onTimer(self):
        pass

class Speaker(Setting):
    pass

class Light(Setting):
    pass

class ScoreBoard(Setting):
    pass
    # def draw(canvas):
    #     canvas.create_rectangle(data.width//2+30, 0, data.width//2+50, 30, fill="blue")
    #     canvas.create_rectangle(data.width//2+200, 0, data.width//2+220, 30, fill="blue")
    #     canvas.create_rectangle(data.width//2, 30, data.width//2+250, 150, fill="blue")
    #     canvas.create_text(data.width//2+125, 70, text=len(data.crowd), font="Arial 18 bold", fill="white")
    #     canvas.create_text(data.width//2+125, 110, text="score: "+str(data.score), font="Arial 18 bold", fill="white")

class DanceFloor(Setting):
    def draw(self, canvas):
        canvas.create_polygon(self.cx-self.width//2, self.cy-self.height//2,self.cx+self.width//2,self.cy-self.height//2,
            self.cx+self.width*2//3, self.cy+self.height//2, self.cx-self.width*2//3, self.cy+self.height//2, outline="red",fill="grey90", width=5)
    pass
            
def isValidSwitch(data):
    cued1 = False
    for cue in data.controller.turntable1.channel.cue:
        if cue.cued:
            cued1 = True
    cued2 = False
    for cue in data.controller.turntable2.channel.cue:
        if cue.cued:
            cued2 = True   
    return cued1 and cued2

def accuracyRating(data):
    distance = None
    for component in data.controller.component:
        if isinstance(component, Turntable):
            if component.channel.isPlayed:
                for cue in component.channel.cue:
                    if cue.cued:
                        distance = abs(component.channel.block.x-cue.x)
    if distance != None:
        data.tempState = [data.currState, distance]

def switch(data):
    accuracyRating(data)
    if isValidSwitch(data):
        mixer.music.stop()
        for component in data.controller.component:
            if isinstance(component, Turntable):
                component.channel.isPlayed = not component.channel.isPlayed
                if component.channel.isPlayed:
                    name = component.musicInfo["name"]
                    loc = (component.channel.block.x-component.channel.start)/component.channel.speed
                    mixer.music.load("music/{}.ogg".format(name))
                    mixer.music.play(1, loc//10)
                    data.startLoc = loc*100
                findCurrState(component, data)
                data.log.append(["switch", data.currState] + data.tempState)
    if data.controller.turntable1.channel.isPlayed:
        for p in data.crowd:
            p.setInfo(data.controller.turntable1.musicInfo)
    else:
        for p in data.crowd:
            p.setInfo(data.controller.turntable2.musicInfo)
    for p in data.crowd:
            p.respond(data.log)
            p.changeState()
    pass

def checkMusic():
    path = "music"
    if os.listdir(path) == []:
        return False
    return True

####################################
# customize these functions
####################################

def initializePerformance(data):
    data.ctrlW = data.width//2
    data.ctrlH = data.height//3
    data.controller = Controller(data.width*3//7, 
        data.height-data.ctrlH//2, data.ctrlW, data.ctrlH)
    data.setting = []
    data.timer = 0
    data.currState = ""
    data.musicInfo = loadMusicInfo()
    data.info = getInfo(data.musicInfo)
    data.controller.display1.table.setInfo(data.info)
    data.controller.display2.table.setInfo(data.info)
    data.currMusic = None
    data.tempState = None
    data.crowd = []
    data.log = []
    data.isPlaying = False
    data.score = 0
    data.heat = 0
    data.thermometer = PhotoImage(file="sources/thermometer.gif")
    data.danceFloor = DanceFloor(data.width//2, data.height//2, 650, 700)
    data.startLoc = 0
    data.numOfSongs = 3
    data.haveMusic = checkMusic()
    if data.haveMusic:
        mixer.init()
    data.bonusScore = 0
    data.limitCrowd = 30

def cue(channel, event):
    if channel.isDisplayed:
        for cue in channel.cue:
            if cue.isClicked(event.x, event.y):
                if channel.cued == False:
                    cue.color = "green"
                    channel.cued = True
                    cue.cued = True
                elif cue.cued == True:
                    cue.color = "red"
                    channel.cued = False
                    cue.cued = False
                if channel.isPlayed == False and cue.cued:
                    channel.block.x = cue.x

def findMusic(data, name):
    for info in data.musicInfo:
        if info["name"] == name:
            return info

def mousePressedPerformance(event, data):
    for component in data.controller.component:
        if isinstance(component, Turntable):
            if component.isClicked(event.x, event.y):
                component.channel.isDisplayed = not component.channel.isDisplayed
                # print(component.channel.isDisplayed)
                break
            cue(component.channel, event)
        if isinstance(component, Display):
            if component.isClicked(event.x, event.y):
                component.table.isDisplayed = not component.table.isDisplayed
            if component.table.isDisplayed:
                component.table.isClicked(event.x, event.y)
                data.currMusic = component.table.choice
                component.table.choice = None
                if data.currMusic != None and data.numOfSongs > 0:
                    music = findMusic(data, data.currMusic)
                    if component == data.controller.display1 and not data.controller.turntable1.channel.isPlayed:
                        data.controller.turntable1.setInfo(music)
                        if data.haveMusic and not mixer.music.get_busy():
                            file = "music/{}.ogg".format(data.currMusic)
                            mixer.music.load(file)
                            data.numOfSongs -= 1
                        data.controller.turntable1.channel.cued = False   
                    elif component == data.controller.display2 and not data.controller.turntable2.channel.isPlayed:
                        data.controller.turntable2.setInfo(music)
                        if data.haveMusic and not mixer.music.get_busy():
                            file = "music/{}.ogg".format(data.currMusic)
                            mixer.music.load(file)
                            data.numOfSongs -= 1
                        data.controller.turntable1.channel.cued = False 
                data.currMusic = None
        if isinstance(component, Equalizer):
            if component.isClicked(event.x, event.y):
                data.log.append(("eq", data.currState))
                for p in data.crowd:
                    p.respond(data.log)
        if isinstance(component, Microphone):
            if component.isClicked(event.x, event.y):
                data.log.append(("mc", data.currState))
                for p in data.crowd:
                    p.respond(data.log)
    if data.controller.fader1.isClicked(event.x, event.y):
        switch(data)
    elif data.controller.fader2.isClicked(event.x, event.y):
        switch(data)


def playMusic(data):
    if not mixer.music.get_busy():
        mixer.music.play()
    else:
        if data.isPlaying == True:
            mixer.music.unpause()
        else:
            mixer.music.pause()
def keyPressedPerformance(event, data):
    if event.keysym == "Up":
        switch(data)
    if event.keysym == "Left":
        if data.controller.turntable2.channel.isPlayed == False: #and data.controller.turntable2.channel.musicLoc != {}:
            data.controller.turntable1.channel.isPlayed = not data.controller.turntable1.channel.isPlayed
            data.isPlaying = not data.isPlaying
            if data.haveMusic:
                playMusic(data)
            for p in data.crowd:
                p.setInfo(data.controller.turntable1.channel.musicLoc)
    if event.keysym == "Right":
        if data.controller.turntable1.channel.isPlayed == False: #and data.controller.turntable2.channel.musicLoc != {}:
            data.controller.turntable2.channel.isPlayed = not data.controller.turntable2.channel.isPlayed
            data.isPlaying = not data.isPlaying
            if data.haveMusic:
                playMusic(data)
            for p in data.crowd:
                p.setInfo(data.controller.turntable2.channel.musicLoc)
    if event.keysym == "Down":
        data.gameState = data.fromState
        mixer.music.stop()
        initializePerformance(data)
        # data.money += data.score//100
        # data.popularity += len(data.crowd)

def findCurrState(component, data):
    musicLoc = component.musicLoc
    currTime = (component.channel.time)*(component.channel.block.x-
        component.channel.start)/component.channel.width
    if component.channel.isPlayed:
        for locs in musicLoc:
            for loc in musicLoc[locs]:
                startPoint = loc[0]
                endPoint = loc[1]
                if startPoint <= currTime <= endPoint+50:
                    data.currState = locs
                    break

def turntableAct(component, data):
    if component.channel.block.x < component.channel.x + component.channel.width//2:
        if component.channel.isPlayed and data.haveMusic:
            x = mixer.music.get_pos()
            component.channel.block.x = component.channel.start+component.channel.width*(x+data.startLoc)/(component.channel.time*100)
        elif component.channel.isPlayed:
            component.channel.moveBlock()

    findCurrState(component, data)

def average(rate):
    return sum(rate)/len(rate)

def timerFiredPerformance(data):
    for component in data.controller.component:
        if isinstance(component, Turntable):
            turntableAct(component, data)
        # if isinstance(component, Display):
        #     displayAct(component, data)
    if data.timer % 50 == 0:
        if data.isPlaying and len(data.crowd) <= data.limitCrowd:
            data.crowd.append(People())
    if data.timer % 10 == 0 and (data.controller.turntable1.channel.isPlayed 
        or data.controller.turntable2.channel.isPlayed):
        rate = []
        for people in data.crowd:
            rate.append(people.rate)
        if rate != []:
            data.heat = average(rate)
    if data.timer % 5 == 0 and data.isPlaying:
        data.score += int(data.heat/5)
    for people in data.crowd:
        people.changeState()
        people.move()
    data.timer += 1
    sortCrowd(data)
    if data.controller.turntable1.channel.block.x == data.controller.turntable1.channel.start+data.controller.turntable1.channel.width or\
        data.controller.turntable2.channel.block.x == data.controller.turntable2.channel.start+data.controller.turntable2.channel.width:
        data.gameState = "studio"
        data.money += data.score//100
        data.popularity += len(data.crowd)
    # if mixer.music.get_busy() == False:
    #     data.gameState = data.fromState
    #     # data.money += data.score//100
    #     # data.popularity += len(data.crowd)



def removePeople(data):
    print(123456)
    for p in data.crowd:
        if p.currState == "leave" and not p.inDanceFloor:
            data.crowd.remove(p)

def sortCrowd(data):
    tempCrowd = data.crowd
    tempLocs = {}
    data.crowd = []
    for p in tempCrowd:
        if p.y in tempLocs:
            tempLocs[p.y] += [p]
        else:
            tempLocs[p.y] = [p]
    sortedLocs = sorted(tempLocs.keys())
    for loc in sortedLocs:
        data.crowd.extend(tempLocs[loc])

def drawScoreBoard(canvas, data):
    canvas.create_rectangle(data.width//2+30, 0, data.width//2+50, 30, fill="blue")
    canvas.create_rectangle(data.width//2+200, 0, data.width//2+220, 30, fill="blue")
    canvas.create_rectangle(data.width//2, 30, data.width//2+250, 150, fill="blue")
    canvas.create_text(data.width//2+125, 50, text="number of people: "+str(len(data.crowd)), font="Arial 18 bold", fill="white")
    canvas.create_text(data.width//2+125, 90, text="score: "+str(data.score), font="Arial 18 bold", fill="white")
    canvas.create_text(data.width//2+125, 130, 
        text=data.log[-1][0] if len(data.log) > 0 else "",
        font="Arial 18 bold", fill="white")


def drawSetting(canvas, data):
    canvas.create_rectangle(0, data.height-150, data.width, data.height, fill="grey37")
    canvas.create_rectangle(150, data.height-275, data.width-150, data.height, fill="grey37")
    canvas.create_polygon(0, data.height//2, 80, data.height//2-60,
        80, data.height//2+220, 0, data.height//2+300, fill="grey13")
    canvas.create_polygon(0, data.height//2, 80, data.height//2-60,
        0, data.height//2-80, fill="grey30")
    canvas.create_polygon(data.width, data.height//2, data.width-80, data.height//2-60,
        data.width-80, data.height//2+220, data.width, data.height//2+300, fill="grey13")
    canvas.create_polygon(data.width, data.height//2, data.width-80, data.height//2-60,
        data.width, data.height//2-80, fill="grey30")
    canvas.create_rectangle(data.width-60, data.height//2+80,
        data.width-20, data.height//2+80+120*(1-data.heat/100),fill="white")
    canvas.create_rectangle(data.width-60, data.height//2+200-120*(data.heat/100),
        data.width-20, data.height//2+200,fill="red")
    canvas.create_image(data.width-40, data.height//2+140, image=data.thermometer)

def redrawAllPerformance(canvas, data):
    data.danceFloor.draw(canvas)
    for p in data.crowd:
        p.draw(canvas)
    # draw in canvas
    drawSetting(canvas, data)
    # data.scoreBoard.draw(canvas)
    drawScoreBoard(canvas, data)
    data.controller.draw(canvas)

