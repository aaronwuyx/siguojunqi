from Tkinter import *
from Defines import *
import board,rule,message
import os,sys

class Client:
    def __init__(self):
        self.status = 'start'
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
    def connecttoServer(self):
#create a thread
        self.wait4Server(self)
    def wait4Server(self):
        return
    def run(self):
        self.connecttoServer(self):
        self.win.mainloop()
        self.conf.Save('filename')

class Configuration:
    def __init__(self,clientname='?',clientaddress = '',clientport=80,servername='localhost',serverport='?'):
        self.name=clientname
        self.address=clientaddress
        self.port=clientport
        self.servername=servername
        self.serverport=serverport
    def Load(self):
        return
    def Save(self):
        return
