import random
from tkinter import *

def mergeTwoDicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

class Member(object):
    def __init__(self):
        self.salary = 1000

    def act(self):
        pass

class VJ(object):
    def __init__(self):
        self.salary = random.randint(15,70)*100

    def act(self):
        return random.randint(self.salary*3//4, self.salary*5//4)*10

class LightControl(Member):
    def __init__(self):
        self.salary = random.randint(50,70)*100

    def act(self):
        return random.randint(self.salary*3//4, self.salary*5//4)

class GhostProducer(Member):
    def __init__(self):
        self.salary = random.randint(15,40)*100

    def act(self):
        name = "ghost track"
        info = {'intro': ([0, 300]), 'verse': ([300, 750], [1430, 1870]), 'buildup': 
            ([750, 890], [1870, 2020]), 'drop': ([890, 1200], [2020, 2330]), 
            'break': ([1200, 1430]), 'outro': ([2330, 2840])}
        info["name"] = name
        info["artist"] = "self"
        info["duration"] = info["outro"][-1]
        return random.randint(self.salary*3//4, self.salary*5//4)*10, info


class Career(object):

    memberTypes = [VJ(), LightControl(), GhostProducer()]
    eqtList = {"headphone":200, "speaker":200, "studio":10000, "synthesizer":1500, "instrument":200}

    def __init__(self):
        self.popularity = 0
        self.money = 50
        self.productionSkill = 20
        self.djskill = 50
        self.musciLib = []
        self.released = []
        self.member = {}
        self.isSigned = False
        self.schedule = [[None for i in range(7)] for j in range(4)]
        self.equipment = {}
        self.initializeEqt()
        self.isFull = False
        self.scheduleManu = False
        self.month = 0
        self.date = -1
        self.cellSize = 50
        self.scheduleColor = {"p":"yellow", "d":"red", "r":"green", "t":"cyan"}
        self.selection = (-1,-1)
        self.x = 500
        self.y = 275
        self.calenderW = 350
        self.calenderH = 200
        self.cellW = self.calenderW/7
        self.cellH = self.calenderH/4
        self.showCalender = False
        self.showShop = False
        self.showProduction = False
        self.showRecruit = False
        self.progress = 0

    def initializeEqt(self):
        self.equipment["headphone"] = random.randint(5,15)
        self.equipment["speaker"] = random.randint(5,20)
        self.equipment["studio"] = random.randint(100,200)
        self.equipment["synthesizer"] = 0
        self.equipment["instrument"] = random.randint(5,15)
        pass

    def nextDay(self):
        self.date += 1
        if self.date > 28:
            self.date = -1
            self.month += 1
        if self.month > 12:
            self.month += 1

    def drawNextDay(self, canvas):
        x = 0
        y = 0
        canvas.create_reactangle(x-50, y-50, x+50, y+50, fill="grey90")
        canvas.create_text(x,y,text="next day", font="Arial 16 bold")

    def train(self):
        self.productionSkill += 100
        self.djskill += 100

    def getScore(self):
        score = 0
        for eqt in self.equipment.keys():
            score += self.equipment[eqt]
        score += self.productionSkill
        return random.randint(score*3//4,score*5//4)

    def validSchedule(self):
        pass

    def isValidProduce(self):
        count = 0
        for week in self.schedule:
            for day in week:
                if day == "yellow":
                    count += 1
        return count-5

    def ghostProduce(self):
        if "ghostProducer" in self.member and len(self.member["ghostProducer"]) > 0:
            salary, info = self.member["ghostProducer"][0].act()
            if self.money - salary < 0:
                self.popularity//=3
                self.member = {}
            else:
                self.money -= salary
                self.musciLib.append(info)
    
    def produce(self):
        self.progress += 1
        if self.progress > 5:
            musicScore = self.getScore()
            name = "ID " + str(len(self.musciLib)+1)
            info = {'intro': ([0, 300]), 'verse': ([300, 750], [1430, 1870]), 'buildup': 
                ([750, 890], [1870, 2020]), 'drop': ([890, 1200], [2020, 2330]), 
                'break': ([1200, 1430]), 'outro': ([2330, 2840])}
            info["name"] = name
            info["artist"] = "self"
            info["duration"] = info["outro"][-1]
            self.musciLib.append(info, musicScore)
            self.productionSkill += 50
            self.progress = 0
        else:
            return
        pass
        # this function produce a new music
        # which is useful for performance and gaining fame
        # this correspond to release music

    def release(self, track):
        self.released.append(track)
        score = track[1]
        if self.signUp:
            self.popularity += random.randint(score,score*5//3)
            self.money += random.randint(score,score*5//3)//10
        else:
            self.popularity += random.randint(score*2//3,score*5//3)//10
            self.money += random.randint(score*2//3,score*4//3)//10
        pass
        # this function release a newly produced music
        # which may gain money or fame
        # the effect of new music also based on current money, and current popularity
        # you can also choose to invest in promoting

    def recruit(self, memberType):
        self.member[memberType] = self.member.get(memberType, 0) + 1
        pass
        # this function recruit new people into your team
        # they may carry out positions like controlling light or visual on the screen(so called VJ)
        # you can also recruit a ghost producer, when you don't have time to produce music
        # but you want to gain fame or money(or the record company demand a track to release but you productionSkillt have one)
        # visuals and lights can add bonus points on performance score
    
    def signUp(self):
        if self.signUp == False:
            if self.popularity > 1000:
                self.signUp == True
        pass
        # this function sign you up to a new record company,
        # which could provide you with money, people, release opportunity,
        # they also set up your performance event schedule, and release schedule
        # you can train yourself faster with a record company

    def purchase(self, eqt):
        self.equipment[eqt] += 10
        pass
        # this function purchase new gears for production or djing
        # any item has the probability of getting broken or being stoled
        # better items can give you bonus scores on each performance/ music release

    def checkFull(self):
        count = 0
        for week in self.schedule:
            for day in week:
                if day == None:
                    count += 1
        return count < 6

    def toSchedule(self, row, col):
        self.full = self.checkFull()
        if self.signUp:
            for week in self.schedule:
                week[-1] = "dj"
                week[-2] = "dj"
                week[-3] = "dj"
            self.schedule[1][-4] = "release"
            self.schedule[3][-4] = "release"
        

        pass
        # this function schedule future performance, production, 
        # training, or other event. If you sign up to a record company, 
        # your schedule will always be have filled(scheduled by the company)
        # where you can't schedule again by yourself.

    def save(self):
        # write a csv file
        pass

    def getCellBounds(self, row, col):
        x0 = self.x-self.calenderW//2+self.cellW*col
        x1 = self.x-self.calenderW//2+self.cellW*(col+1)
        y0 = self.y-self.calenderH//2+self.cellH*row
        y1 = self.y-self.calenderH//2+self.cellH*(row+1)
        return x0, y0, x1, y1

    def drawSchedule(self, canvas):
        if self.date >= 0:
            r = self.date//7
            c = self.date%7
        else:
            r = -1
            c = -1
        for row in range(len(self.schedule)):
            for col in range(len(self.schedule[0])):
                x0, y0, x1, y1 = self.getCellBounds(row, col)
                if (row, col) == self.selection and self.schedule[row][col] == None:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="brown", width=5 if (row, col) == (r,c) else 1, outline= "yellow" if (row, col) == (r,c) else "")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill=self.schedule[row][col] if self.schedule[row][col] != None else "grey70", 
                        width=5 if (row, col) == (r,c) else 1, outline= "yellow" if (row, col) == (r,c) else "")

                canvas.create_text(x0+self.cellW//2, y0+self.cellH//2, text=str(col+1), font="Arial 20 bold")
        pass

