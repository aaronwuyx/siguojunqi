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
        self.menus = {}
        self.toolbutton = []
        self.remain = ''
        rule.PlaceOne( self.conf.place, self.map, self.conf.player )

    def run( self ):
        self.make_gui()
        self.top.mainloop()
        self.closeConnection()
        self.conf.Save( 'default.cfg' )

    def closeConnection( self ):
        if self.socket:
            message.writeline( self.socket, 'Disconnect:' + str( self.conf.player ) )
            self.socket.close()

    def GUI_disconnect( self ):
        if self.socket:
            if askyesno( 'Warning', 'Do you really want to disconnect?' ):
                self.closeConnection()

    def createConnection( self ):
        if self.socket == None:
            self.socket = socket( AF_INET, SOCK_STREAM )
            self.socket.connect( ( self.conf.host, self.conf.port ) )
            message.writeline( self.socket, str( self.conf.player ) )
            data, self.remain = message.readline( self.socket, self.remain )
            cmd, arg, obj = message.splitline( data )
            if cmd == 'error':
                self.socket.close()
                self.socket = None
                print obj
                raise Exception( str( obj ) )

    def GUI_connect( self ):
        def jump( ignore = None ):
            ent2.focus()
            ent2.select_range( 0, END )

        def fetch( ignore = None ):
            self.conf.host = s.get()
            self.conf.port = i.get()
            try:
                self.createConnection()
                t.destroy()
            except Exception as exc:
                showerror( 'Error', str( exc ) )

        t = Toplevel()
        t.title( 'Connect server' )
        b = Frame( t )
        b.pack( side = BOTTOM, expand = YES, fill = X )
        Button( b, text = 'Connect', command = fetch ).pack( side = LEFT )
        Button( b, text = 'Cancel', command = t.destroy ).pack( side = RIGHT )
        lab = Frame( t, bd = 2 )
        lab.pack( side = LEFT, expand = YES, fill = Y )
        Label( lab, text = 'Host address' ).pack( side = TOP )
        Label( lab, text = 'Port' ).pack( side = TOP )
        ent = Frame( t, bd = 2 )
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
        Main = Menu( self.top )
        self.top.config( menu = Main )
        self.menus['main'] = Main
        Option = Menu( Main, tearoff = 0 )
        Option.add_command( label = 'Discard', command = ( lambda: 0 ), underline = 0 )
        Option.add_command( label = 'Load', command = ( lambda: 0 ), underline = 0 )
        Option.add_command( label = 'Save', command = ( lambda: 0 ), underline = 0 )
        Option.add_command( label = 'Name...', command = self.GUI_name, underline = 0 )
        color = IntVar()
        color.set( self.conf.player )
        def setPlayer( x ):
            rule.CleanOne( self.map, self.conf.player )
            self.conf.player = x
            rule.PlaceOne( self.conf.place, self.map, self.conf.player )
            self.board.Draw_Map( self.map, self.conf.player )
        Bgcolor = Menu( Option, tearoff = 0 )
        Bgcolor.add_radiobutton( label = 'Red', variable = color, value = 1, command = ( lambda : setPlayer( 1 ) ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Yellow', variable = color, value = 2, command = ( lambda: setPlayer( 2 ) ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Green', variable = color, value = 3, command = ( lambda: setPlayer( 3 ) ), underline = 0 )
        Bgcolor.add_radiobutton( label = 'Blue', variable = color, value = 4, command = ( lambda: setPlayer( 4 ) ), underline = 0 )
        Option.add_cascade( label = 'Colour', menu = Bgcolor, underline = 0 )
        Option.add_command( label = 'Rule', command = ( lambda:0 ), underline = 0 )
        Main.add_cascade( label = 'Option', menu = Option, underline = 0 )
        self.menus['option'] = Option

        Game = Menu( Main, tearoff = 0 )
        Game.add_command( label = 'Save', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Load', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Connect', command = self.GUI_connect, underline = 0 )
        Game.add_command( label = 'Disconnect...', command = self.GUI_disconnect, underline = 0 )
        Game.add_command( label = 'Review', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Yield', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Quit', command = ( lambda:0 ), underline = 0 )
        Game.add_command( label = 'Exit', command = self.top.quit, underline = 1 )
        Main.add_cascade( label = 'Game', menu = Game, underline = 0 )
        self.menus['game'] = Game

        Help = Menu( Main, tearoff = 0 )
        Help.add_command( label = 'Help', command = ( lambda:0 ), underline = 0 )
        Help.add_separator()
        Help.add_command( label = 'License...', command = self.GUI_license, underline = 0 )
        Help.add_command( label = 'About...', command = self.GUI_about, underline = 0 )
        Main.add_cascade( label = 'Help', menu = Help, underline = 0 )
        self.menus['help'] = Help
        for name, menu in self.menus.items():
            menu.config( bg = '#eeeeee', fg = '#111111', activebackground = '#ffffff', activeforeground = '#000000', disabledforeground = '#666666', postcommand = self.updateMenuToolbar )

    def add_toolbar( self ):
        self.toolbar = Frame()
        self.toolbutton.append( Button( self.toolbar, text = 'Exit', command = self.top.quit ) )
        self.toolbutton.append( Button( self.toolbar, text = 'Connect 连接', command = self.GUI_connect ) )
        self.toolbutton.append( Button( self.toolbar, text = 'Test', command = self.GUI_test ) )
        for button in self.toolbutton:
            button.pack( side = RIGHT )
            Label( text = ' ' ).pack( side = RIGHT )
            button.config( width = 15, relief = RAISED )
        self.toolbar.pack( side = TOP, expand = YES, fill = X )
        self.toolbar.config( relief = GROOVE, bd = 2, background = 'white' )

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
            self.conf.name = s.get()
            t.destroy()

        t = Toplevel()
        t.title( 'Option' )
        b = Frame( t, bd = 2 )
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
        self.add_sidebar()
        self.board = board.Board( self.top, self.conf )
        self.board.Draw_Map( self.map , self.conf.player )
        self.guiopt.release()

    def add_sidebar( self ):
        self.statusframe = Frame( self.top )
        self.statusframe.pack( side = RIGHT, expand = YES, fill = Y )
        self.statusframe.config( relief = GROOVE, bd = 1, bg = 'white' )
        self.moveframe = Frame( self.statusframe )
        Label( self.moveframe, text = 'Move :' ).pack( side = TOP, expand = YES, fill = X )
        but = Frame( self.moveframe, bd = 1 )
        def execute():
            try:
                f = string.atoi( self.movef.get() )
                t = string.atoi( self.movet.get() )
                if DEBUG:
                    print 'from = ', f, 'to = ', t
                    print 'Available ? ', self.map.Move( f, t )
                if self.map.Move( f, t ):
                    self.board.Draw_Map( self.map, self.conf.player )
            except:
                pass
        Button( but, text = 'exec', command = execute ).pack( side = LEFT, anchor = W )
        def clear():
            self.movef.set( '' )
            self.movet.set( '' )
        Button( but, text = 'clear', command = clear ).pack( side = RIGHT, anchor = E )
        but.pack( side = BOTTOM, expand = YES, fill = X )
        lab = Frame( self.moveframe, bd = 1 )
        ent = Frame( self.moveframe, bd = 1 )
        Label( lab, text = 'From' ).pack( side = TOP, anchor = NW )
        Label( lab, text = 'To' ).pack( side = TOP, anchor = NW )
        self.movef = StringVar()
        self.movet = StringVar()
        self.movef.set( '' )
        self.movet.set( '' )
        Entry( ent, textvariable = self.movef ).pack( side = TOP, expand = YES, fill = X )
        Entry( ent, textvariable = self.movet ).pack( side = TOP, expand = YES, fill = X )
        lab.pack( side = LEFT )
        ent.pack( side = RIGHT )
        self.moveframe.pack( side = TOP )

    def GUI_test( self ):
        message.writeline( self.socket, 'Hello, this is a test!' )

if __name__ == '__main__':
    c = Client()
    c.run()
