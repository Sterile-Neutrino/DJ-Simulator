from tkinter import *
from Career import *

class Program(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 100

    def isClicked(self, x, y):
        return self.x - self.size//2 <= x < self.x + self.size//2 and \
            self.y - self.size//2 <= y <= self.y + self.size//2

    def act(self):
        pass

class Production(Program):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.isDisplayed = False
        self.icon = PhotoImage()
        self.currState = None
        self.length = 1500
    def act(self):
        sample = {'intro': [0, 300], 'verse': ([300, 750], [1430, 1870]), 'buildup': 
            ([750, 890], [1870, 2020]), 'drop': ([890, 1200], [2020, 2330]), 
            'break': [1200, 1430], 'outro': [2330, 2840]}
        return sample

class Shop(Program):
    def __init__(self, x, y):
        self.items = Career.eqtList

    def purchase(self):
        pass

class recruit(Program):
    