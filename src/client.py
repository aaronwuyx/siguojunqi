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
from socket import *
from defines import *
import board, rule, message
import os, sys, thread, time, string

class Client():
    def __init__( self ):
        self.conf = Configuration()
        self.conf.Load( 'default.cfg' )
        self.guiopt = thread.allocate_lock()
        self.map = rule.Map( len( Pos4 ) )
        self.socket = None
        rule.PlaceOne( self.conf.place, self.map, self.conf.player )

    def run( self ):
        self.make_gui()
        self.top.mainloop()
        if self.socket:
            self.socket.close()
        self.conf.Save( 'default.cfg' )

    def GUI_connect( self ):
        def jump( ignore = None ):
            ent2.focus()
            ent2.select_range( 0, END )

        def fetch( ignore = None ):
            self.conf.host = s.get()
            self.conf.port = i.get()
            try:
                self.socket = socket( AF_INET, SOCK_STREAM )
                self.socket.connect( ( self.conf.host, self.conf.port ) )
                #self.toserver = self.socket.makefile( 'w', 0 )
                t.destroy()
            except:
                showerror( 'Error', 'Cannot connect to server.\n' )

        t = Toplevel()
        t.title( 'Connect server' )
        b = Frame( t )
        b.pack( side = BOTTOM, expand = YES, fill = X )
        Button( b, text = 'Connect', command = fetch ).pack( side = LEFT )
        Button( b, text = 'Cancel', command = t.destroy ).pack( side = RIGHT )
        lab = Frame( t )
        lab.pack( side = LEFT, expand = YES, fill = Y )
        Label( lab, text = 'Host address' ).pack( side = TOP )
        Label( lab, text = 'Port' ).pack( side = TOP )
        ent = Frame( t )
        ent.pack( side = RIGHT, expand = YES, fill = BOTH )
        s = StringVar()
        i = IntVar()
        s.set( self.conf.host )
        i.set ( self.conf.port )
        ent1 = Entry( ent, textvariable = s )
        ent2 = Entry( ent, textvariable = i )
        ent1.bind( '<Return>', jump )
        ent2.bind( '<Return>', fetch )
        ent1.pack( side = TOP, expand = YES, fill = X )
        ent1.select_range( 0, END )
        ent2.pack( side = TOP, expand = YES, fill = X )
        ent1.focus()
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def make_gui( self ):
        self.top = Tk()
        self.top.title( 'SiGuo client program - player : ' + self.conf.name )
        self.add_menus()
        self.add_toolbar()
        self.add_widgets()

    def add_menus( self ):
        self.menu = Menu( self.top )
        self.top.config( menu = self.menu )
        File = Menu( self.menu )
        File.add_command( label = 'New', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Load', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Save', command = ( lambda: 0 ), underline = 0 )
        File.add_command( label = 'Connect', command = self.GUI_connect, underline = 0 )
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
        Bgcolor = Menu( Option, tearoff = 0 )
        Bgcolor.add_radiobutton( label = 'Red', command = ( lambda:0 ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Yellow', command = ( lambda:0 ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Green', command = ( lambda:0 ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Blue', command = ( lambda:0 ), underline = 0 )
        Option.add_cascade( label = 'Background Color', menu = Bgcolor, underline = 0 )
        Option.add_command( label = 'Rule', command = ( lambda:0 ), underline = 0 )
        self.menu.add_cascade( label = 'Option', menu = Option, underline = 0 )
        Help = Menu( self.menu )
        Help.add_command( label = 'Help', command = ( lambda:0 ), underline = 0 )
        Help.add_separator()
        Help.add_command( label = 'License', command = self.GUI_license, underline = 0 )
        Help.add_command( label = 'About', command = self.GUI_about, underline = 0 )
        self.menu.add_cascade( label = 'Help', menu = Help, underline = 0 )

    def add_toolbar( self ):
        self.toolbar = Frame()
        Button( self.toolbar, text = 'exit', command = self.top.quit ).pack( side = RIGHT )
        self.toolbar.pack( side = TOP )

    def updateMenuToolbar( self ):
        return

    def GUI_about( self ):
        t = Toplevel()
        t.title( 'About SiGuo' )
        Label( t, text = 'SiGuo svn ' + SVN + '\n' + VERSION ).pack( side = TOP )
        Label( t, text = ' You can find source code in http://code.google.com/p/siguojunqi/' ).pack( side = TOP )
        Button( t, text = 'OK', command = t.destroy ).pack( side = RIGHT )
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def GUI_license( self ):
        t = Toplevel()
        t.title( 'License' )
        Button( t, text = 'OK', command = t.destroy ).pack( side = BOTTOM )
        l = Text( t )
        l.pack()
        t.grab_set()
        t.focus_set()
        t.wait_window()

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
        self.board.Draw_Map( self.map , self.conf.player )
        self.guiopt.release()

class Configuration:
    def __init__( self, name = 'Unknown', bgcolor = 'red' ):
        self.name = name
        self.bgcolor = bgcolor
        self.player = 1
        self.placefile = 'place.cfg'
        self.place = getDefaultPlace( self.player )
        self.host = 'localhost'
        self.port = 30000

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
                    try:
                        self.bgcolor = string.atoi( value )
                    except:
                        pass
                if key == 'place':
                    self.placefile = value
                if key == 'host':
                    self.host = value
                if key == 'port':
                    try:
                        self.port = string.atoi( value )
                    except:
                        pass
            except:
                pass
        try:
            f.close()
        except:
            pass
        backfile = self.placefile
        backplace = self.place
        if self.loadPlace( self.placefile ):
            if not ( rule.CheckPlace1( self.place ) & rule.CheckPlace2( self.place ) ):
                self.placefile = backfile
                self.place = backplace
        else:
            self.placefile = backfile
            self.place = backplace

    def Save( self, filename ):
        try:
            f = open( filename, 'w' )
        except:
            return
        f.write( 'siguo game client configuration:\n' )
        f.write( 'name=' + self.name + '\n' )
        f.write( 'bg=' + self.bgcolor + '\n' )
        f.write( 'place=' + self.placefile + '\n' )
        try:
            f.close()
        except:
            pass
        self.savePlace( self.placefile )

    def loadPlace( self, filename ):
        try:
            f = open ( filename, 'r' )
        except:
            return
        place = []
        for line in f.readlines():
            for item in line.split():
                try:
                    if item == 'None':
                        place.append( MapItem() )
                    else:
                        place.append( MapItem( string.atoi( item ), self.player , MAP_HIDE ) )
                except:
                    return
        return place

    def savePlace( self, filename ):
        try:
            f = open( filename, 'w' )
        except:
            return False
        for place in self.place:
            f.write( str( place.getValue() ) + ' ' )
        f.write( '\n' )
        return True


if __name__ == '__main__':
    c = Client()
#    rule.PlaceOne( c.conf.place, c.map, 2 )
#    rule.PlaceOne( c.conf.place, c.map, 3 )
#    rule.PlaceOne( c.conf.place, c.map, 4 )
    c.run()
