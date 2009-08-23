"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from Tkinter import *
from defines import *
import board, rule, message
import os, sys, thread, time

class Client():
    def __init__( self ):
        self.conf = Configuration()
        self.conf.Load( 'default.cfg' )
        self.map = rule.Map( len( Pos4 ) )
        #self.status = 'start'
        #then connect to server, get seat, create a new thread to receive message?
        #self.seq = ???
        self.guiopt = thread.allocate_lock()
        self.guiexit = thread.allocate_lock()
    def make_gui( self ):
        self.guiexit.acquire()
        self.top = Tk()
        self.top.title( 'Si Guo Client - player : ' + self.conf.name )
        self.add_menus()
        self.add_widgets()
        self.top.mainloop()
        self.guiexit.release()
    def add_menus( self ):
        self.menu = Menu( self.top )
        self.top.config( menu = self.menu )
        file = Menu( self.menu )
        file.add_command( label = 'New', command = ( lambda: 0 ), underline = 0 )
        file.add_command( label = 'Load', command = ( lambda: 0 ), underline = 0 )
        file.add_command( label = 'Save', command = ( lambda: 0 ), underline = 0 )
        file.add_command( label = 'Connect', command = ( lambda: 0 ), underline = 0 )
        file.add_command( label = 'Exit', command = self.top.quit, underline = 1 )
        self.menu.add_cascade( label = 'File', menu = file, underline = 0 )
        game = Menu( self.menu )
        game.add_command( label = 'Save', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Load', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Review', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Yield', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Quit', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Game', menu = game, underline = 0 )
        option = Menu( self.menu )
        option.add_command( label = 'Name', command = ( lambda:0 ), underline = 0 )
        option.add_command( label = 'Color', command = ( lambda:0 ), underline = 0 )
        option.add_command( label = 'Rule', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Option', menu = option, underline = 0 )
        help = Menu( self.menu )
        help.add_command( label = 'Help', command = ( lambda:0 ), underline = 0 )
        help.add_command( label = 'About', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Help', menu = help, underline = 0 )
    def add_widgets( self ):
        status = Frame( self.top )
        status.pack( side = RIGHT )
        Label( status, text = 'status :' ).pack()
        self.guiopt.acquire()
        self.board = board.Board( self.top )
        self.guiopt.release()
    def connecttoServer( self ):
#create a thread
        self.wait4Server( self )
    def wait4Server( self ):
        return
    def run( self ):
        self.PlaceAll()
#        self.connecttoServer( self )
        thread.start_new( self.make_gui, () )
        time.sleep( 1 )
        while self.guiexit.locked():
            pass
        self.conf.Save( 'default.cfg' )
    def PlaceAll( self ):
#        self.getPlace() get data from player / file?
#        self.map.place(...)
        return

class Configuration:
    def __init__( self, clientname = '?', clientaddress = '', clientport = 80, servername = 'localhost', serverport = '?' ):
        self.name = clientname
        self.address = clientaddress
        self.port = clientport
        self.servername = servername
        self.serverport = serverport
    def Load( self, filename ):
        return
    def Save( self, filename ):
        return

if __name__ == '__main__':
    Client().run()

