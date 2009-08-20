from Defines import *
import rule
import message
import os,sys

class Server:
    def __init__(self):
        self.client=[]
    def wait4Connection(self):
        while True:
            s = Message().receive()
            if s.cmd == 'connect':
                self.client.append()
                #create for new thread...
                if len(self.client) == MAXPLAYER:
                    break
            elif s.cmd == 'disconnect':
                #kill the thread...
                self.client.remove()
            else continue
    def run(self):
        self.wait4Connection()
        return

if __name__=='__main__':
    s = Server()
    s.run()
