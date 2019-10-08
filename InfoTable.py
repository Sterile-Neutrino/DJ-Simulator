import csv

def decode(s):
    if s == "None":
        return None
    if "; " in s:
        s1, s2 = s.split("; ")
        return decode(s1)+decode(s2)
    elif "," in s:
        lst = s.split(",")
        return [(int(lst[0])*10, int(lst[1])*10)]

def loadMusicInfo():
    with open('musicInfo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        musicInfo = []
        for row in csv_reader:
            musicInfo.append(row)
    tempInfo = musicInfo[2:]
    musicInfo = []
    for row in tempInfo:
        musicDict = {}
        musicDict["name"] = row[1]
        musicDict["artist"] = row[2]
        musicDict["intro"] = decode(row[3])
        musicDict["verse"] = decode(row[4])
        musicDict["buildup"] = decode(row[5])
        musicDict["drop"] = decode(row[6])
        musicDict["break"] = decode(row[7])
        musicDict["outro"] = decode(row[8])
        musicDict["duration"] = musicDict["outro"][0][1]
        musicDict["genre"] = row[9]
        musicInfo.append(musicDict)
    return musicInfo
    


# for dict_ in musicInfo:

# Animation Starter Code, Focus on timerFired

from tkinter import *

####################################
# customize these functions
####################################

def getInfo(generalInfo):
    info = []
    for dict_ in generalInfo:
        newD = {}
        newD["name"] = dict_["name"]
        newD["artist"] = dict_["artist"]
        newD["duration"] = dict_["duration"]
        newD["genre"] = dict_["genre"]
        info.append(newD)
    return info

class InfoTable(object):
    def __init__(self, x=500, y=300, info={}):
        self.x = x
        self.y = y
        self.width = 400
        self.height = 200
        self.row = 4
        self.rowH = self.height//self.row
        self.col = 4
        self.colW = self.width//self.col
        self.width//4
        self.displayInfo = info
        self.start = 0
        self.choice = None
        self.prev = Button(self.x-self.width//2+self.colW//2, 
            self.y+self.height//2+self.rowH//2, self.colW, self.rowH, "Prev")
        self.next = Button(self.x+self.width//2-self.colW//2, 
            self.y+self.height//2+self.rowH//2, self.colW, self.rowH, "Next")
        self.isDisplayed = False
    
    def setInfo(self, info):
        self.displayInfo = info

    def draw(self, canvas):
        if self.isDisplayed:
            info = self.displayInfo[self.start:]
            for i in range(self.start+self.row):
                if i < len(info):
                    infoRow = info[i]
                    j = 0
                    for infoTag in infoRow.keys():
                        x0 = self.x - self.width//2 + self.colW*j
                        y0 = self.y - self.height//2 +self.rowH*i
                        x1 = self.x - self.width//2 + self.colW*(j+1)
                        y1 = self.y - self.height//2 +self.rowH*(i+1)
                        canvas.create_rectangle(x0,y0,x1,y1,fill="orange")
                        canvas.create_text(x0+self.colW//2, y0+self.rowH//2,
                            text=infoRow[infoTag][:13] if isinstance(infoRow[infoTag], str) else infoRow[infoTag])
                        j += 1
                elif i < 4:
                    canvas.create_rectangle(self.x-self.width//2, self.y - self.height//2 +self.rowH*i,
                        self.x + self.width//2, self.y - self.height//2 +self.rowH*(i+1), fill="orange")
            self.prev.draw(canvas)
            canvas.create_rectangle(self.x-self.width//2+self.colW, 
                self.y+self.height//2, self.x+self.width//2-self.colW, self.y+self.height//2+self.rowH, fill="orange")
            self.next.draw(canvas)
    def isClicked(self, x, y):
        if self.isDisplayed:
            if self.prev.isClicked(x,y):
                if self.start >= 4:
                    self.start -= 4
            elif self.next.isClicked(x,y):
                if len(self.displayInfo) - self.start - 4> 0:
                    self.start += 4
            self.choice = self.getRow(x, y)

    def getRow(self, x, y):
        info = self.displayInfo[self.start:]
        for i in range(self.start+self.row):
            if i < len(info):
                infoRow = info[i]
                j = 0
                for infoTag in infoRow.keys():
                    x0 = self.x - self.width//2 + self.colW*j
                    y0 = self.y - self.height//2 +self.rowH*i
                    x1 = self.x - self.width//2 + self.colW*(j+1)
                    y1 = self.y - self.height//2 +self.rowH*(i+1)
                    if x0 <= x <= x1 and y0 <= y <= y1:
                        self.choice = infoRow["name"]
        if self.choice != None:
            self.isDisplayed = False
            return self.choice
        return None




class Button(object):
    def __init__(self, cx, cy, w, h, text):
        self.width = w
        self.height = h
        self.cx = cx
        self.cy = cy
        self.text = text

    def isClicked(self, x, y):
        return self.cx-self.width//2 <= x <= self.cx+self.width//2 and \
            self.cy-self.height//2 <= y <= self.cy+self.height//2
        pass

    def act(self, data):
        pass

    def draw(self, canvas):
        # draw the block of the button
        canvas.create_rectangle(self.cx-self.width//2, self.cy-self.height//2, 
            self.cx+self.width//2, self.cy+self.height//2, fill="orange")
        canvas.create_text(self.cx, self.cy, text=self.text)
