# -*- coding:utf-8 -*-
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
import tkMessageBox
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
        help.add_command( label = 'About', command = self.GUI_about, underline = 0 )
        self.menu.add_cascade( label = 'Help', menu = help, underline = 0 )
    def add_widgets( self ):
        status = Frame( self.top )
        status.pack( side = RIGHT )
        Label( status, text = 'status :' ).pack()
        self.guiopt.acquire()
        self.board = board.Board( self.top )
        self.board.Draw_Map( self.map )
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
    def GUI_about( self ):
        tkMessageBox.showinfo( 'About', 'SiGuo game\nSVN ' + SVN + '\n' );

class Configuration:
    def __init__( self, name = 'Unknown', bgcolor = 'red' ):
        self.name = name
        self.bgcolor = bgcolor
#        self.ip = self.getIPAddress()
#        self.port = xxx?
#        self.server = ( 'localhost', 2000 )
#        self.address = clientaddress
#        self.port = clientport
#    def getIPAddress( self ):
#        return 'localhost'

    def config( self ):
        return

    def Load( self, filename ):
        if not os.path.isfile( filename ):
            return
        try:
            f = open( filename, 'r' )
        except:
            return
        for line in f.readlines():
            try:
                key, value = line.split( filename , 1 )
                key = key.strip()
                value = value.strip()
                if key == 'name':self.name = value
                if key == 'bg':self.bgcolor = value
            except:
                pass
        try:
            f.close()
        except:
            pass

    def Save( self, filename ):
        try:
            f = open( filename, 'w' )
            f.writeline( 'siguo game client configuration:' )
            f.writeline( 'name=' + self.name )
            f.writeline( 'bg=' + self.bgcolor )
            f.close()
        except:
            pass

if __name__ == '__main__':
    c = Client()
    c.map.Place( 0, 40, 1 )
    c.map.Place( 10, 39, 1 )
    c.map.Place( 20, 38, 1 )
    c.map.Place( 30, 37, 2 )
    c.map.Place( 40, 36, 2 )
    c.map.Place( 50, 35, 2 )
    c.map.Place( 60, 34, 3 )
    c.map.Place( 70, 33, 3 )
    c.map.Place( 80, 32, 3 )
    c.map.Place( 90, 42, 4 )
#    c.map.Place( 100, 36, 2 )
#    c.map.Place( 110, 35, 2 )
    c.run()

#        tkMessageBox.Message( message = 'aa' ).show();
