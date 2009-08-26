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
from tkMessageBox import *
from defines import *
import board, rule, message
import os, sys, thread, time

class Client():
    def __init__( self ):
        self.conf = Configuration()
        self.conf.Load( 'default.cfg' )
        self.guiopt = thread.allocate_lock()
        self.guiexit = thread.allocate_lock()
        self.map = rule.Map( len( Pos4 ) )

    def run( self ):
        thread.start_new( self.make_gui, () )
        thread.start_new( self.connect_server, () )
        #then connect to server, get seat, create a new thread to receive message?
        #self.seq = ???
        time.sleep( 1 )
        while self.guiexit.locked():
            pass
        self.conf.Save( 'default.cfg' )

    def make_gui( self ):
        self.guiexit.acquire()
        self.top = Tk()
        self.top.title( 'SiGuo client program - player : ' + self.conf.name )
        self.add_menus()
        self.add_widgets()
        self.top.mainloop()
        self.guiexit.release()

    def add_menus( self ):
        self.menu = Menu( self.top )
        self.top.config( menu = self.menu )
        File = Menu( self.menu )
        File.add_command( label = 'New', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Load', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Save', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Connect', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Exit', command = self.top.quit, underline = 1 )
        self.menu.add_cascade( label = 'File', menu = File, underline = 0 )
        Game = Menu( self.menu )
        Game.add_command( label = 'Save', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Load', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Review', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Yield', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Quit', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Game', menu = Game, underline = 0 )
        Option = Menu( self.menu )
        Option.add_command( label = 'Name', command = self.GUI_name, underline = 0 )
        Option.add_command( label = 'Background Color', command = ( lambda:0 ), underline = 0 )
        Option.add_command( label = 'Rule', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Option', menu = Option, underline = 0 )
        Help = Menu( self.menu )
        Help.add_command( label = 'Help', command = ( lambda:0 ), underline = 0 )
        Help.add_separator()
        Help.add_command( label = 'License', command = self.GUI_license, underline = 0 )
        Help.add_command( label = 'About', command = self.GUI_about, underline = 0 )
        self.menu.add_cascade( label = 'Help', menu = Help, underline = 0 )

    def GUI_about( self ):
        t = Toplevel()
        t.title( 'About SiGuo' )
        Label( t, text = 'SiGuo svn ' + SVN + VERSION ).pack( side = TOP )
        Button( t, text = 'OK', command = t.quit ).pack( side = RIGHT )
        t.mainloop()

    def GUI_license( self ):
        t = Toplevel()
        t.title( 'License' )
        Button( t, text = 'OK', command = t.quit ).pack( side = BOTTOM )
        t.mainloop()

    def GUI_name( self ):
        def fetch( ignore = None ):
            self.conf.name = ent.get()
            t.destroy()

        t = Toplevel()
        t.title( 'Option' )
        b = Frame( t )
        b.pack( side = BOTTOM, expand = YES, fill = X )
        Button( b, text = 'ok', command = fetch ).pack( side = LEFT )
        Button( b, text = 'cancel', command = t.destroy ).pack( side = RIGHT )
        Label( t, text = 'Name' ).pack( side = LEFT )
        s = StringVar()
        s.set( self.conf.name )
        ent = Entry( t, textvariable = s )
        ent.bind( '<Return>', fetch )
        ent.pack( side = RIGHT, expand = YES, fill = X )
        ent.focus()
        ent.select_range( 0, END )
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def add_widgets( self ):
        self.guiopt.acquire()
        self.statusframe = Frame( self.top )
        self.statusframe.pack( side = RIGHT, expand = YES, fill = Y )
        Label( self.statusframe, text = 'status :' ).pack( side = TOP, expand = YES, fill = X )
        self.board = board.Board( self.top )
        self.board.Draw_Map( self.map )
        self.guiopt.release()

    def connect_server( self ):
        return

"""

    def PlaceAll( self ):
#        self.getPlace() get data from player / file?
#        self.map.place(...)
        return
"""

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
        try:
            f = open( filename, 'r' )
        except:
            return
        for line in f.readlines():
            try:
                key, value = line.split( '=' , 1 )
                key = key.strip()
                value = value.strip()
                if key == 'name':
                    self.name = value
                if key == 'bg':
                    self.bgcolor = value
            except:
                pass
        try:
            f.close()
        except:
            pass

    def Save( self, filename ):
        try:
            f = open( filename, 'w' )
        except:
            return
        f.write( 'siguo game client configuration:\n' )
        f.write( 'name=' + self.name + '\n' )
        f.write( 'bg=' + self.bgcolor + '\n' )
        try:
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
    c.run()
