from Tkinter import *
import os
import sys
from defines import *
def Game():
    w = Toplevel()
    w.title('Game')
    Board(w)
    w.mainloop()
    
class Board(Frame):
    def __init__(self,parent = None,**config):
        Frame.__init__(self,parent,config)
        self.pack()
        self.drawmap()
        self.drawpositions()
    def drawmap(self):
        #Canvas
        return
    def drawpositions(self):
        for pos in Pos4:
            self.drawposition(pos)
        return
    def drawposition(self,position,highlight = False):
        print position
        #draw a rectangle at x y?
        return
    
if __name__=='__main__':
    Game()
