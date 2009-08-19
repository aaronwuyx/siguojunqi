from Tkinter import *
from defines import *

class Board(Frame):
    def __init__(self,parent = None,**config):
        Frame.__init__(self,parent,config)
        self.pack(expand =YES,fill=BOTH)
        self.draw_Map()
        self.draw_Positions()
    def draw_Map(self):
        #Canvas
        return
    def draw_Positions(self):
        for pos in Pos4:
            self.drawposition(pos)
        return
    def drawposition(self,position,highlight = False):
        print position
        #draw a rectangle at x y?
        return
    def draw_Chess(self,somedata):
        return

if __name__=='__main__':
    Board().mainloop()
