# Animation Starter Code, Focus on timerFired

from tkinter import *
from Career import *
from MainManu import *
from Performance import *
from Studio import *

####################################
# customize these functions
####################################

def initializeStudio(data):
    # load data.xyz as appropriate
    data.career = Career()
    data.studio = PhotoImage(file="sources/studio.gif")
    data.isDisplaying = False
    pass

def mousePressedStudio(event, data):
    # use event.x and event.y
    if 240 <= event.x <= 280 and 150 <= event.y <= 190:
        data.career.showProduction = not data.career.showProduction
    elif 240 <= event.x <= 280 and 200 <= event.y <= 240:
        data.career.showShop = not data.career.showShop
    elif 240 <= event.x <= 280 and 250 <= event.y <= 290:
        data.career.showRecruit = not data.career.showRecruit
    elif 240 <= event.x <= 280 and 300 <= event.y <= 340:
        data.career.signUp()
    elif 240 <= event.x <= 280 and 350 <= event.y <= 390:
        data.career.showCalender = not data.career.showCalender
        if data.career.showCalender == False:
            data.career.selection = (-1,-1)
    elif 700 <= event.x <= 740 and 350 <= event.y <= 390:
        data.career.nextDay()
        r,c = data.career.date//7, data.career.date%7
        if data.career.schedule[r][c] == "cyan":
            data.career.train()
        elif data.career.schedule[r][c] == "yellow":
            data.career.produce()
        elif data.career.schedule[r][c] == "green":
            music = data.career.musicLib[-1]
            if music not in data.career.released:
                data.career.release(music)
            else:
                data.career.money -= 3000
        elif data.career.schedule[r][c] == "red":
            data.gameState = "performance"
            data.fromState = 'studio'


    if 500-350//2 <= event.x <= 500+350//2 and 275-200//2 <= event.y <= 275+200//2 and data.career.showCalender:
        col = (event.x-(500-350//2))//data.career.cellW
        row = (event.y-(275-200//2))//data.career.cellH
        data.career.selection = (int(row), int(col))
    pass

def keyPressedStudio(event, data):
    # use event.char and event.keysym
    print(data.career.selection)
    if data.career.showCalender:
        print(data.career.checkFull)
        if data.career.selection != (-1, -1) and not data.career.checkFull():
            row = data.career.selection[0]
            col = data.career.selection[1]
            data.career.schedule[row][col] = data.career.scheduleColor[event.keysym]
    if event.keysym == "Down":
        data.gameState = "main"
    pass

def timerFiredStudio(data):
    pass

def redrawAllStudio(canvas, data):
    # draw in canvas
    canvas.create_image(data.width//2, data.height//2, image=data.studio)
    if data.career.showCalender:
        data.career.drawSchedule(canvas)
    canvas.create_oval(240, 150, 280, 190, fill="yellow")
    canvas.create_oval(240, 200, 280, 240, fill="blue")
    canvas.create_oval(240, 250, 280, 290, fill="purple")
    canvas.create_oval(240, 300, 280, 340, fill="green")
    canvas.create_oval(240, 350, 280, 390, fill="orange")
    canvas.create_oval(700, 350, 740, 390, fill="silver")
    canvas.create_text(data.width//2, 100, text="popularity: "+str(data.career.popularity), font="Arial 20 bold", fill="white")
    canvas.create_text(data.width//3, 50, text="money: "+str(data.career.money), font="Arial 20 bold", fill="white")
    canvas.create_text(data.width*2//3, 50, text="skill: "+str(data.career.productionSkill)+"    "+str(data.career.djskill), font="Arial 20 bold", fill="white")
    canvas.create_text(data.width//2, 700, text="members: "+repr(data.career.member), font="Arial 20 bold", fill="white")
    pass
