from tkinter import *
from MainManu import *
from Performance import *
from Studio import *

def init(data):
    # load data.xyz as appropriate
    data.gameState = "main"
    data.fromState = "main"
    initializeMainManu(data)
    initializePerformance(data)
    initializeStudio(data)

def mousePressed(event, data):
    # use event.x and event.y
    if data.gameState == "main": mousePressedMainManu(event, data)
    if data.gameState == "performance": mousePressedPerformance(event, data)
    if data.gameState == "studio": mousePressedStudio(event, data)
    # if data.controller.turntable1.isClicked
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.gameState == "main": keyPressedMainManu(event, data)
    if data.gameState == "performance": keyPressedPerformance(event, data)
    if data.gameState == "studio": keyPressedStudio(event, data)
    pass

def timerFired(data):
    if data.gameState == "main": timerFiredMainManu(data)
    if data.gameState == "performance": timerFiredPerformance(data)
    if data.gameState == "studio": timerFiredStudio(data)
    pass

def redrawAll(canvas, data):
    if data.gameState == "main": redrawAllMainManu(canvas, data)
    if data.gameState == "performance": redrawAllPerformance(canvas, data)
    if data.gameState == "studio": redrawAllStudio(canvas, data)


# cited from 15112 course note
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

run(1000, 750)