from Tkinter import *
from Defines import *
import Board
import os,sys

class Client:
    def __init__(self):
        self.conf = Configuration()
        self.conf.Load('filename')
        self.pl = Player(self.conf.name)
        #then connect to server, get seat, create a new thread to receive message?
        #self.seq = ???
        self.make_widgets()
    def make_widgets(self):
#new thread and create widget?
        self.win = Toplevel()
        self.win.title('Si Guo - Player :'+self.pl.name)
        status = Frame()
        status.pack(side=RIGHT)
        self.board = Board(self.win)
        self.board.draw_Chess(self.pl)
    def ReceiveMessage(self):
        return
    def run(self):
        self.win.mainloop()
        self.conf.Save('filename')

class Configuration:
    def __init__(self,name='?',server='localhost'):
        self.name=name
        self.servername=server
    def Load(self):
        return
    def Save(self):
        return
