import random
from tkinter import *

class People(object):
    acceptableSwitch = [
        ("outro", "intro"), ("buildup", "drop"),
        ("drop", "break"), ("break", "verse"),
        ("verse", "buildup"), ("drop", "intro"),
        ("break", "intro"), ("drop", "drop")
    ]
    acceptableEq = [
        "buildup", "drop", "verse", "break"
    ]
    groove = ["Future House", "Bass House", "Progressive House", "Tech House"]
    repetitive = ["Techno", "Progressive House", "Trance"]
    pop = ["Future Bass"]
    heavy = ["Bass House", "Dubstep", "Metalstep", "Brostep", "Riddim Dubstep"]
    banger = ["Metalstep", "Brostep", "EDM Trap", "Trapstep", "Big House"]
    acceptableMc = [
        "buildup", "drop", "verse"
    ]
    first = False
    head = []
    walk = []
    dance = []
    def __init__(self):
        self.x = 0
        self.y = 0
        self.spawnX = 0
        self.spawnY = 0
        self.spawn()
        self.onFloor = True
        self.state = "prep"
        self.taste = random.choice([People.groove, People.repetitive, People.pop, People.heavy, People.banger])
        self.rate = 70
        self.info = None
        if People.first == False:
            People.head = [PhotoImage(file="sources/head1.gif"), PhotoImage(file="sources/head2.gif"), PhotoImage(file="sources/head3.gif")]
            People.walk = [PhotoImage(file="sources/walk1.gif"), PhotoImage(file="sources/walk2.gif")]
            People.dance = [PhotoImage(file="sources/dance1.gif"), PhotoImage(file="sources/dance2.gif")]
            People.first = True
        self.range = random.randint(10,20)
        self.head = random.choice(People.head)
        self.walk = People.walk
        self.dance = People.dance
        self.currBody = self.walk[0]
        self.locx = random.randint(500-330, 500+330)
        self.locy = random.randint(375-280, 375+250)
        self.danceMove = 0
        self.limitEq = 2
        self.limitMc = 2

    def spawn(self):
        self.x = random.randint(-50, 1050)
        self.spawnX = self.x
        if 500-325 < self.x < 500+325:
            self.y = random.randint(-50,0)
            self.spawnY = self.y
        else:
            self.y = random.randint(-50, 500)
            self.spawnY = self.y
        pass

    def inDanceFloor(self):
        return 500-325 < self.x < 500+325 and 375-350 < self.y < 375+300
        pass

    def changeState(self):
        # if position inside dance floor (random position)
        # change state to "dance"
        # if rate is below 30
        # 1-rate//100 percent of change state to "leave"
        # if postion outside the screen
        # change onFloor to False
        # a function in main will remove this person from the list crowd
        if self.state == "prep":
            if self.inDanceFloor():
                if self.locx-20 <= self.x <= self.locx+20 and self.locy-20 <= self.y <= self.locy+20:
                    self.state = "dance"
        if self.state == "dance":
            if self.rate < 30:
                self.state = "leave"
            pass

    def move(self):
        # if state is "prep"
        # move toward the direction of the dj controller
        if self.state == "prep":
            if self.x < self.locx-5:
                self.x += 5
            elif self.x > self.locx+5:
                self.x -= 5
            else:
                self.x += 0
            if self.y < self.locy-5:
                self.y += 5
            elif self.y > self.locy+5:
                self.y -= 5
            else:
                self.y += 0
            if self.currBody == self.walk[0]:
                self.currBody = self.walk[1]
            else:
                self.currBody = self.walk[0]
        # if state is "dance"
        # have dance moves:
        # small position move and body moves
        if self.state == "dance":
            self.danceMove += 1
            if self.danceMove%50 < 25:
                self.currBody = self.dance[0]
            else:
                self.currBody = self.dance[1]
        if self.state == "leave":
            if self.x < self.locx-5:
                self.x -= 5
            elif self.x > self.locx+5:
                self.x += 5
            else:
                self.x += 0
            if self.y < self.locy-5:
                self.y -= 5
            elif self.y > self.locy+5:
                self.y += 5
            else:
                self.y += 0
            if self.currBody == self.walk[0]:
                self.currBody = self.walk[1]
            else:
                self.currBody = self.walk[0]
        # if state is "leave"
        # move toward the opposite direction of dj controller

    def respond(self, log):
        # each person respond to DJ's operation based on the quality of performance
        # and their own taste
        # the function takes in the last row of log
        # which represent the lastest thing the DJ have done
        # compute the response and change the person's rate of the performance accordingly
        if log != []:
            operation = log[-1]
            typeOfOperation = operation[0]
            if typeOfOperation == "switch":
                self.limitMc = 2
                self.limitEq = 2
                genre = self.info["genre"]
                if genre in self.taste:
                    self.rate += 5
                    if self.rate > 100:
                        self.rate == 100
                afterSection = operation[1]
                beforeSection = operation[2]
                accuracy = operation[3]
                switch = (beforeSection, afterSection)
                if switch in People.acceptableSwitch:
                    if accuracy <= self.range:
                        self.rate += 10
                        if self.rate > 100:
                            self.rate = 100
                    elif accuracy <= self.range*2:
                        self.rate += 10*self.range//accuracy
                    else:
                        self.rate -= 5
                        if self.rate < 0:
                            self.rate = 0
                else:
                    self.rate -= 20
                    if self.rate < 0:
                        self.rate = 0
            elif typeOfOperation == "eq":
                section = operation[1]
                self.limitEq -= 1
                if section in People.acceptableEq and self.limitMc > 0:
                    self.rate += 5
                    if self.rate > 75:
                        self.rate = 75
                else:
                    self.rate -= 10
                    if self.rate < 0:
                        self.rate = 0
            elif typeOfOperation == "mc":
                section = operation[1]
                self.limitMc -= 1
                if section in People.acceptableMc and self.limitMc > 0:
                    self.rate += 5
                    if self.rate > 75:
                        self.rate = 75
                else:
                    self.rate -= 10
                    if self.rate < 0:
                        self.rate = 0
        pass

    def setInfo(self, info):
        self.info = info

    def draw(self, canvas):
        # call different draw function in different state
        # the function play different loops of moves by presenting different image
        # note: open all image in init!!!
        # draw function was called hundreds and thousands of time in the program
        # if opening image in draw function, the image will leave behind in the memory
        # the take up enormous amount of space until memory overflows
        if self.state == "dance":
            if self.danceMove % 50 < 25:
                canvas.create_image(self.x, self.y+40, image=self.currBody)
            else:
                canvas.create_image(self.x, self.y+10, image=self.currBody)
            canvas.create_image(self.x, self.y-30, image=self.head)
        else:
            canvas.create_image(self.x, self.y+40, image=self.currBody)
            canvas.create_image(self.x, self.y-30, image=self.head)
        pass
