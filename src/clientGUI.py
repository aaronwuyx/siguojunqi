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

import os
from tkinter import *
from tkinter.messagebox import askyesno, showerror
from tkinter.filedialog import askopenfilenames
from tkinter.colorchooser import askcolor

import define
from profile import Profile
from board import Board

def Startup():
    return tk_Startup()

def tk_Startup():
    Tk().withdraw()
    ret = None

    def Create():
        nonlocal ret
        if define.DEBUG:
            print( s1.get(), ' ', s2.get() )
        if ( s1.get() != '' ) & ( int( s2.get() ) in range( define.MAXPLAYER ) ):
            name = s1.get()
            id = s2.get()
            p = Profile( name )
            p.id = id
            if os.path.exists( p.filename ):
                showerror( 'Error', 'profile already exist' )
                return
            p.save()
            t.destroy()
            ret = p.filename
        else:
            showerror( 'Error', 'invalid argument' )

    def Load():
        nonlocal ret
        fname = askopenfilenames( title = 'Load your profile', filetypes = [ ( 'Profile', '*.cfg' ) ] )
        if fname != '':
            t.destroy()
            ret = fname[1:-1]

    def Exit():
        t.destroy()
        sys.exit()

    t = Toplevel()
    t.title( 'Startup' )
    btn = Frame( t, relief = RAISED )
    btn.pack( side = RIGHT, expand = YES, fill = Y, ipadx = 1, ipady = 1 )
    Button( btn, text = 'Create', width = 10, command = Create ).pack( side = TOP )
    Button( btn, text = 'Load', width = 10, command = Load ).pack( side = TOP )
    Button( btn, text = 'Exit', width = 10, command = Exit ).pack( side = TOP )
    lab = Frame( t, relief = RAISED )
    lab.pack( side = LEFT, expand = YES, fill = BOTH, ipadx = 1, ipady = 1 )
    Label( lab, text = 'Name:' ).grid( column = 0, row = 0 )
    Label( lab, text = 'Side:' ).grid( column = 0, row = 1 )
    Label( lab, text = 'GUI:' ).grid( column = 0, row = 3 )
    s1 = StringVar()
    s2 = IntVar()
    s3 = IntVar()
    Entry( lab, textvariable = s1, bd = 1 ).grid( column = 1, row = 0, sticky = E )
    side = Frame( lab )
    side.grid( column = 1, row = 1 , rowspan = 2 )
    Radiobutton( side, text = 'Red', variable = s2, value = 0 ).grid( column = 0, row = 0, sticky = W )
    Radiobutton( side, text = 'Yellow', variable = s2, value = 1 ).grid( column = 1, row = 0, sticky = W )
    Radiobutton( side, text = 'Green', variable = s2, value = 2 ).grid( column = 0, row = 1, sticky = W )
    Radiobutton( side, text = 'Blue', variable = s2, value = 3 ).grid( column = 1, row = 1, sticky = W )
    gui = Frame( lab )
    gui.grid( column = 1, row = 3 )
    Radiobutton( gui, text = 'Tk', variable = s3, value = 0 ).pack( side = LEFT )
    s1.set( '' )
    s2.set( 0 )
    s3.set( 0 )
    t.focus_set()
    t.grab_set()
    t.wait_window()
    return ret

class clientGUI( Toplevel ):

    def __init__( self , client ):
        Toplevel.__init__( self )
        self.client = client
        self.toolbarbutton = {}
        self.menu = {}
        self.init( client )

    def init( self, client ):
        if client:
            self.title( 'SiGuo client - ' + client.prof.name )
        else:
            self.title( 'SiGuo client' )
        self.protocol( 'WM_DELETE_WINDOW', self.GUI_Exit )
        self.config( bg = 'white' )
        self.add_menu()
        self.add_toolbar()
        self.add_sidebar()
        self.add_board()
        self.add_events()

    #one way to tell other widgets about value changes, use virtual events
    #another is widget.after(...)
    def add_events( self ):
        self.event_add( '<<name>>' , '<Button-2>' , 'n', 'a' )
        self.bind( '<<name>>', self.onNameChange )
        self.event_add( '<<id>>' , '<Button-2>' , 'i', 'd' )
        self.bind( '<<id>>', self.onIdChange )
        self.event_add( '<<color>>' , '<Button-2>' , 'c', 'o' )
        self.bind( '<<color>>', self.onColorChange )

    def add_menu( self ):
        main = Menu( self )
        self.config( menu = main )
        self.menu['main'] = main

        game = Menu( main )
        game.add_command( label = 'Connect', command = self.GUI_Connect, underline = 0 )
        game.add_command( label = 'Yield', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Disconnect', command = self.GUI_Disconnect, underline = 0 )
        game.add_separator()
        game.add_command( label = 'Save', command = ( lambda:0 ), underline = 0 )
        game.add_command( label = 'Load', command = ( lambda:0 ), underline = 0 )
        game.add_separator()
        game.add_command( label = 'Exit', command = self.GUI_Exit, underline = 1 )
        self.menu['game'] = game
        main.add_cascade( label = 'Game', menu = game, underline = 0 )

        option = Menu( main )
        option.add_command( label = 'Reload', command = self.GUI_Reload, underline = 0 )
        option.add_command( label = 'Save', command = ( lambda: 0 ), underline = 0 )
        option.add_command( label = 'Load', command = ( lambda: 0 ), underline = 0 )
        option.add_separator()
        option.add_command( label = 'Profile', command = self.GUI_Profile, underline = 0 )
        option.add_command( label = 'Rule', command = ( lambda: 0 ), underline = 2 )
        self.menu['option'] = option
        main.add_cascade( label = 'Option', menu = option, underline = 0 )

        view = Menu( main )
        self.menu['view'] = view
        for item in ['self.view_move', 'self.view_log', 'self.view_record', 'self.view_msg', 'self.view_player']:
            exec( item + '= IntVar()' )
            exec( item + '.set(1)' )
        view.add_checkbutton( label = 'Record', variable = self.view_record, underline = 0 )
        view.add_checkbutton( label = 'Player', variable = self.view_player, underline = 0 )
        view.add_checkbutton( label = 'Message', variable = self.view_msg, underline = 0 )
        view.add_separator()
        view.add_checkbutton( label = 'DEBUG: Move', variable = self.view_move, underline = 0 )
        view.add_checkbutton( label = 'DEBUG: Log', variable = self.view_log, underline = 0 )
        main.add_cascade( label = 'View', menu = view, underline = 0 )

        helps = Menu( main )
        helps.add_command( label = 'Help', command = self.GUI_Help, underline = 0 )
        helps.add_separator()
        helps.add_command( label = 'License', command = self.GUI_License, underline = 0 )
        helps.add_command( label = 'About', command = self.GUI_About, underline = 0 )
        self.menu['help'] = helps
        main.add_cascade( label = 'Help', menu = helps, underline = 0 )

        for ( name, menu ) in self.menu.items():
            menu.config( bg = 'white', fg = 'black', activebackground = 'blue', activeforeground = 'white', disabledforeground = 'grey', tearoff = 0, postcommand = self.Update_MenuToolbar )

        self.menu['game'].entryconfig( 1, state = DISABLED )
        self.menu['game'].entryconfig( 2, state = DISABLED )
        self.menu['game'].entryconfig( 4, state = DISABLED )

    def add_toolbar( self ):
        self.toolbar = Frame( self )
        self.toolbar.pack( side = BOTTOM, expand = YES, fill = X , anchor = S )
        self.toolbar.config( relief = FLAT, bd = 1, padx = 1, pady = 1, bg = 'white' )

        self.toolbarbutton['exit'] = Button( self.toolbar, text = 'Exit', command = self.GUI_Exit )
        self.toolbarbutton['connect'] = Button( self.toolbar, text = 'Connect', command = self.GUI_Connect )
        self.toolbarbutton['disconnect'] = Button( self.toolbar, text = 'Disconnect', command = self.GUI_Disconnect )
        self.toolbarbutton['test'] = Button( self.toolbar, text = 'TEST ONLY!!!', command = self.GUI_Test )
        for ( name, button ) in self.toolbarbutton.items():
            button.pack( side = RIGHT )
            button.config( width = 15, relief = GROOVE )
            Label( text = ' ' ).pack( side = RIGHT )

    def add_sidebar( self ):
        self.sidebar = Frame( self )
        self.sidebar.pack( side = RIGHT, expand = YES, fill = Y, anchor = E )
        self.sidebar.config( relief = FLAT, bd = 1, padx = 1, pady = 1, bg = 'white' )
        self.add_move( self.sidebar )
        self.add_user( self.sidebar )
        self.add_log( self.sidebar )
        self.add_msg( self.sidebar )

    def add_move( self, master ):
        def execute():
            try:
                f = int( self.movef.get() )
                t = int( self.movet.get() )
                if DEBUG:
                    print( 'from = ', f, 'to = ', t )
            except:
                pass
        def clear():
            self.movef.set( '' )
            self.movet.set( '' )

        self.side_move = Frame( master )
        self.movef = StringVar()
        self.movet = StringVar()
        Label( self.side_move, text = 'Movement' ).grid( column = 0, row = 0, columnspan = 3 )
        Label( self.side_move, text = 'FROM' ).grid( column = 0, row = 1, sticky = W )
        Label( self.side_move, text = ' TO ' ).grid( column = 0, row = 2, sticky = W )
        Button( self.side_move, text = 'exec', command = execute ).grid( column = 0, row = 3, sticky = W )
        Button( self.side_move, text = 'clear', command = clear ).grid( column = 2, row = 3, sticky = E )
        Entry( self.side_move, textvariable = self.movef ).grid( column = 1, row = 1, columnspan = 2 )
        Entry( self.side_move, textvariable = self.movet ).grid( column = 1, row = 2, columnspan = 2 )
        self.movef.set( '' )
        self.movet.set( '' )
        self.side_move.pack( side = TOP, expand = YES, fill = X )
        self.side_move.config( bd = 1 , relief = GROOVE )

    def add_user( self, master ):
        self.side_user = Frame( master )
        Label( self.side_user, text = 'Player' ).pack( side = TOP, expand = YES, fill = X )
        l = Listbox( self.side_user, height = 5 )
        l.insert( END, 'Name' )
        l.insert( END, 'Hi,' )
        l.insert( END, 'it' )
        l.insert( END, 'is' )
        l.insert( END, 'unavailable' )
        l.pack( side = LEFT, expand = YES, fill = X )
        m = Listbox( self.side_user, height = 5, width = 6 )
        m.insert( END, 'Color' )
        m.insert( END, 'Hi,' )
        m.insert( END, 'it' )
        m.insert( END, 'is' )
        m.insert( END, 'unavailable' )
        m.pack( side = RIGHT, expand = YES, fill = X )
        self.side_user.pack( side = TOP, expand = YES, fill = X )
        self.side_user.config( bd = 1 , relief = GROOVE )

    def add_log( self, master ):
        self.side_log = Frame( master )
        Label( self.side_log, text = 'Log' ).pack( side = TOP, expand = YES, fill = X )
        self.side_log_listbox = Listbox( self.side_log, bg = 'white', height = 10 )
        self.side_log_listbox.pack( side = TOP, expand = YES, fill = BOTH )
        self.side_log.pack( side = TOP, expand = YES, fill = X )
        self.side_log.config( bd = 1 , relief = GROOVE )

    def add_msg( self , master ):
        self.side_msg = Frame( master )
        Label( self.side_msg, text = 'Message' ).grid( row = 0, column = 0, columnspan = 3, sticky = EW )
        self.side_msg_text = Text( self.side_msg, bg = 'white', height = 10 )
        self.side_msg_text.grid( row = 1, column = 0, columnspan = 3, rowspan = 2, sticky = NSEW )
        s = StringVar()
        s.set( '' )
        Label( self.side_msg, text = 'Enter here:' ).grid( row = 3, column = 0, sticky = W )
        ent = Entry( self.side_msg, textvariable = s, bg = 'white' )
        ent.grid( row = 3, column = 1, columnspan = 2, sticky = EW )
        self.side_msg.pack( side = TOP, expand = YES, fill = X )
        self.side_msg.config( bd = 1 , relief = GROOVE )

    def Update_MenuToolbar( self ):
        return

    def add_board( self ):
        self.board = Board( self , bg = 'white', bd = 1, relief = FLAT )
        self.board.pack( side = LEFT, expand = YES, fill = BOTH )
        self.board.SetClient( self.client )
        self.board.Draw_Background()

    def GUI_Connect( self ):
        def jump( ignore = None ):
            nonlocal ent2
            ent2.focus()
            ent2.select_range( 0, END )

        def fetch( ignore = None ):
            nonlocal s
            nonlocal i
            nonlocal ent1
            host = s.get()
            port = int( i.get() )
            self.client.Connection_Create( host, port )
            if self.client.socket:
                self.client.prof.host = host
                self.client.prof.port = port
                t.destroy()
            else:
                showerror( 'Error' , 'Connection not created,\nView logs for more detail' )
                ent1.focus()

        t = Toplevel()
        t.title( 'Connect server' )
        b = Frame( t )
        b.pack( side = BOTTOM, expand = YES, fill = X )
        Button( b, text = 'Connect', command = fetch, width = 10 ).pack( side = LEFT )
        Button( b, text = 'Cancel', command = t.destroy, width = 10 ).pack( side = RIGHT )
        lab = Frame( t, bd = 2 )
        lab.pack( side = LEFT, expand = YES, fill = Y )
        Label( lab, text = 'Host address' ).pack( side = TOP )
        Label( lab, text = 'Port' ).pack( side = TOP )
        ent = Frame( t, bd = 2 )
        ent.pack( side = RIGHT, expand = YES, fill = BOTH )
        s = StringVar()
        i = IntVar()
        s.set( self.client.prof.host )
        i.set( self.client.prof.port )
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

    def GUI_Disconnect( self ):
        if askyesno( 'Warning', 'Close connection and quit the game?' ):
            self.client.Connection_Close()

    def GUI_Reload( self ):
        return

    def GUI_Profile( self ):
        def fetch( quit ):
            nonlocal name, id, color
            if name.get() != '':
                self.client.prof.name = name.get()
                self.event_generate( '<<name>>' )
            else:
                showerror( 'Error', 'Name should not be empty' )
                name.set( self.client.prof.name )
                return
            if id.get() in range( define.MAXPLAYER ):
                self.client.prof.id = int( id.get() )
                id.set( self.client.prof.id )
                self.event_generate( '<<id>>' )
            else:
                showerror( 'Error', 'Id should be in 0..3' )
                return
            try:
                exp.config( bg = color.get() )
                self.client.prof.bg = color.get()
                self.event_generate( '<<color>>' )
            except TclError:
                color.set( self.client.prof.bg )
                exp.config( bg = self.client.prof.bg )
            self.client.prof.save()
            if quit:
                t.destroy()

        def Select():
            nonlocal color
            c = askcolor()
            if c:
                try:
                    color.set( c[1] )
                    exp.config( bg = color.get() )
                    self.client.prof.bg = color.get()
                    self.event_generate( '<<color>>' )
                except TclError:
                    color.set( self.client.prof.bg )
                    exp.config( bg = self.client.prof.bg )

        t = Toplevel( bg = 'white' )
        t.title( 'Profile' )
        lab = Frame( t, bg = 'white' )
        lab.pack( side = LEFT, expand = YES, fill = Y )
        Label( lab, text = 'Name', bg = 'white' ).pack( side = TOP )
        Label( lab, text = 'Id', bg = 'white' ).pack( side = TOP )
        Label( lab, text = 'Color', bg = 'white' ).pack( side = TOP )
        btn = Frame( t, relief = GROOVE, bg = 'white' )
        btn.pack( side = BOTTOM, expand = YES, fill = X )
        Button( btn, text = 'OK', command = ( lambda : fetch( True ) ), width = 10 ).pack( side = LEFT, anchor = SW )
        Button( btn, text = 'Cancel', command = t.destroy, width = 10 ).pack( side = LEFT, anchor = SW )
        Button( btn, text = 'Apply', command = ( lambda : fetch( False ) ), width = 10 ).pack( side = LEFT, anchor = SW )
        ent = Frame( t )
        ent.pack( side = RIGHT, expand = YES, fill = BOTH )
        name = StringVar()
        id = IntVar()
        color = StringVar()
        name.set( self.client.prof.name )
        id.set( self.client.prof.id )
        color.set( self.client.prof.bg )
        e1 = Entry( ent, textvariable = name )
        e1.pack( side = TOP, expand = YES, fill = X, anchor = NW )
        e1.bind( '<Return>', ( lambda : fetch( True ) ) )
        e1.focus()
        e1.select_range( 0, END )
        idf = Frame( ent )
        idf.pack( side = TOP, expand = YES, fill = X, anchor = NW )
        Radiobutton( idf, text = '0', variable = id, value = 0 ).pack( side = LEFT )
        Radiobutton( idf, text = '1', variable = id, value = 1 ).pack( side = LEFT )
        Radiobutton( idf, text = '2', variable = id, value = 2 ).pack( side = LEFT )
        Radiobutton( idf, text = '3', variable = id, value = 3 ).pack( side = LEFT )
        clf = Frame( ent )
        clf.pack( side = TOP, expand = YES, fill = X, anchor = NW )
        clr = Entry( clf, textvariable = color, width = 7 )
        clr.pack( side = LEFT, anchor = NW )
        exp = Entry( clf , width = 12 )
        exp.pack( side = LEFT, anchor = NW )
        Button( clf, text = 'Select', command = Select, width = 10 ).pack( side = RIGHT, anchor = NE )
        exp.config( bg = color.get() )
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def GUI_License( self ):
        t = Toplevel()
        t.title( 'License' )
        Button( t, text = 'Close', command = t.destroy, width = 15 ).pack( side = BOTTOM, anchor = SE )
        l = Text( t , bg = 'white' )
        ybar = Scrollbar( t )
        ybar.config( command = l.yview, relief = SUNKEN )
        l.config( yscrollcommand = ybar.set )
        ybar.pack( side = RIGHT, expand = YES, fill = Y )
        l.pack( side = LEFT, expand = YES, fill = BOTH )
        text = ''
        try:
            text = open( 'license.txt', 'r' ).read()
        except:
            showerror( 'Error', 'cannot find license.txt' )
        l.delete( '1.0', END )
        l.insert( '1.0', text )
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def GUI_Help( self ):
        return

    def GUI_About( self ):
        t = Toplevel()
        t.title( 'About SiGuo' )
        lab = Frame( t, bg = 'white' )
        btn = Frame( t, bg = '#cccccc' )
        btn.pack( side = BOTTOM, expand = YES, fill = X )
        lab.pack( side = TOP, expand = YES, fill = BOTH )
        Label( lab, text = 'SiGuo game ' + define.STABLEVERSION + ' revision ' + define.STABLESVN, bg = 'white' ).pack( side = TOP, anchor = NW )
        Label( lab, text = ' You can find source code in http://code.google.com/p/siguojunqi/', bg = 'white' ).pack( side = TOP, anchor = NW )
        Button( btn, text = 'OK', command = t.destroy, width = 15 ).pack( side = RIGHT, anchor = SE )
        t.grab_set()
        t.focus_set()
        t.wait_window()

    def GUI_Test( self ):
        tmp = define.Lineup( 0 )
        tmp.SetToDefault()
        self.client.map.Dump( tmp )
        tmp = define.Lineup( 1 )
        tmp.SetToDefault()
        self.client.map.Dump( tmp, 30 )
        tmp = define.Lineup( 2 )
        tmp.SetToDefault()
        self.client.map.Dump( tmp, 60 )
        tmp = define.Lineup( 3 )
        tmp.SetToDefault()
        self.client.map.Dump( tmp, 90 )
        self.board.Draw_Chess()

    def GUI_Exit( self ):
        if askyesno( 'Warning', 'Do you really want to exit?' ):
            self.quit()

    """
    def GUI_Discard( self ):
        if self.status == CLIENT_INIT:
            if tkMessageBox.askyesno( 'Warning', 'Discard all changes?' ):
                rule.CleanOne( self.map, self.conf.player )
                self.conf.place = GetDefaultPlace( self.conf.player )
                rule.PlaceOne( self.conf.place, self.map, self.conf.player )
                self.board.Draw_Map( self.map, self.conf.player )
                
        def execute():
            try:
                f = int( self.movef.get() )
                t = int( self.movet.get() )
                if DEBUG:
                    print( 'from = ', f, 'to = ', t )
                #    print( 'Available ? ', self.map.Move( f, t ) )
                #if self.map.Move( f, t ):
                #    self.board.Draw_Map( self.map, self.conf.player )
            except:
                pass
    """

    def onNameChange( self, event ):
        self.title( 'SiGuo client - ' + self.client.prof.name )

    def onIdChange( self, event ):
        self.board.Draw_Chess()

    def onColorChange( self, event ):
        return

if __name__ == '__main__':
    import client
    Tk().withdraw()
    c = client.Client()
    c.run()
