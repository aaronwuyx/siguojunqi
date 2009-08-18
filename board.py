from Tkinter import *
import os
import sys
from defines import *

class Board(Frame):
    def __init__(self,parent = None,**config):
        Frame.__init__(self,parent,config)
        self.pack()
        self.drawmap()
        self.drawpositions()
    def drawmap(self):
        return
    def drawpositions(self):
        return
    def drawposition(self,position):
        return
    
if __name__=='__main__':
    Board().mainloop()
