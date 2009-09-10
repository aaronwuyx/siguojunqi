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
try:
    from Tkinter import *
    from tkMessageBox import askyesno, showerror
    from tkFileDialog import askopenfilenames
    from tkColorChooser import askcolor
except ImportError:
    from tkinter import *
    from tkinter.messagebox import askyesno, showerror
    from tkinter.filedialog import askopenfilenames
    from tkinter.colorchooser import askcolor

import define
from profile import Profile
from board import Board

def Startup():
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
            #patch under python 3.1.1
            if type( fname ) == type( str() ):
                ret = fname[1:-1] #under Windows, fname is a string
            else:
                ret = fname[0] #under Linux, fname is a tuple

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
    if ret == None:
        sys.exit()
    return ret

class clientGUI( Toplevel ):

    def __init__( self , client ):
        Toplevel.__init__( self )
        self.client = client
        self.lift()
        self.maxsize()
        self.init( client )

    def init( self, client ):
        if client:
            self.title( 'SiGuo client - ' + client.prof.name )
        else:
            self.title( 'SiGuo client' )
        self.protocol( 'WM_DELETE_WINDOW', self.GUI_Exit )
        self.config( bg = 'white' )

        self.frm_mov = None
        self.frm_log = None
        self.frm_msg = None
        self.frm_usr = None

        self.menu = {}
        self.add_menu()
        self.toolbarbutton = {}
        self.add_toolbar()
        self.columnconfigure( 0, weight = 1, minsize = 500 )
        self.columnconfigure( 1, pad = 1, minsize = 200 )
        self.rowconfigure( 0, weight = 1, minsize = 500 )
        self.rowconfigure( 1, pad = 1 )
        self.add_sidebar()
        self.add_board()
        self.add_events()
        self.minsize( width = 750, height = 550 )

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
        option.add_command( label = 'Save As', command = ( lambda: 0 ), underline = 5 )
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

    def Update_MenuToolbar( self ):
        if self.client.stat == define.CLI_INIT:
            self.menu['game'].entryconfig( 0, state = NORMAL )
            self.menu['game'].entryconfig( 1, state = DISABLED )
            self.menu['game'].entryconfig( 2, state = DISABLED )
            self.menu['game'].entryconfig( 4, state = DISABLED )
            self.menu['game'].entryconfig( 5, state = DISABLED )
            self.menu['game'].entryconfig( 7, state = NORMAL )
            self.menu['option'].entryconfig( 0, state = NORMAL )
            self.menu['option'].entryconfig( 1, state = NORMAL )
            self.menu['option'].entryconfig( 2, state = NORMAL )
            self.menu['option'].entryconfig( 3, state = NORMAL )
        elif self.client.stat == define.CLI_MOVE:
            self.menu['game'].entryconfig( 0, state = DISABLED )
            self.menu['game'].entryconfig( 1, state = NORMAL )
            self.menu['game'].entryconfig( 2, state = NORMAL )
            self.menu['game'].entryconfig( 4, state = DISABLED )
            self.menu['game'].entryconfig( 5, state = DISABLED )
            self.menu['game'].entryconfig( 7, state = NORMAL )
            self.menu['option'].entryconfig( 0, state = DISABLED )
            self.menu['option'].entryconfig( 1, state = DISABLED )
            self.menu['option'].entryconfig( 2, state = DISABLED )
            self.menu['option'].entryconfig( 3, state = DISABLED )
        elif self.client.stat == define.CLI_WAIT:
            self.menu['game'].entryconfig( 0, state = DISABLED )
            self.menu['game'].entryconfig( 1, state = NORMAL )
            self.menu['game'].entryconfig( 2, state = NORMAL )
            self.menu['game'].entryconfig( 4, state = DISABLED )
            self.menu['game'].entryconfig( 5, state = DISABLED )
            self.menu['game'].entryconfig( 7, state = NORMAL )
            self.menu['option'].entryconfig( 0, state = DISABLED )
            self.menu['option'].entryconfig( 1, state = DISABLED )
            self.menu['option'].entryconfig( 2, state = DISABLED )
            self.menu['option'].entryconfig( 3, state = DISABLED )

    def add_toolbar( self ):
        self.toolbar = Frame( self, relief = GROOVE, bd = 1, padx = 1, pady = 1, bg = 'white' )
        self.toolbar.grid( column = 0, row = 1, columnspan = 2, sticky = EW )

        self.toolbarbutton['exit'] = Button( self.toolbar, text = 'Exit', command = self.GUI_Exit )
        self.toolbarbutton['connect'] = Button( self.toolbar, text = 'Connect', command = self.GUI_Connect )
        self.toolbarbutton['disconnect'] = Button( self.toolbar, text = 'Disconnect', command = self.GUI_Disconnect )
        self.toolbarbutton['test'] = Button( self.toolbar, text = 'TEST ONLY!!!', command = self.GUI_Test )
        for ( name, button ) in self.toolbarbutton.items():
            button.pack( side = RIGHT )
            button.config( width = 15, relief = GROOVE )
            Label( text = ' ' ).pack( side = RIGHT )

    def add_sidebar( self ):
        self.sidebar = Frame( self, relief = GROOVE, bd = 1, padx = 1, pady = 1, bg = 'white' )
        self.sidebar.grid( column = 1, row = 0, sticky = NS )

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

        self.frm_mov = Frame( master, bd = 1, relief = RIDGE )
        self.frm_mov.pack( side = TOP, expand = YES, fill = X )
        self.movef = StringVar()
        self.movet = StringVar()
        Label( self.frm_mov, text = 'Movement' ).grid( column = 0, row = 0, columnspan = 3, sticky = EW )
        Label( self.frm_mov, text = 'From' ).grid( column = 0, row = 1, sticky = W )
        Label( self.frm_mov, text = 'To' ).grid( column = 0, row = 2, sticky = W )
        Button( self.frm_mov, text = 'Execute', command = execute, width = 10 ).grid( column = 1, row = 3, sticky = W )
        Button( self.frm_mov, text = 'Clear', command = clear, width = 10 ).grid( column = 2, row = 3, sticky = E )
        Entry( self.frm_mov, textvariable = self.movef ).grid( column = 1, row = 1, columnspan = 2, sticky = EW )
        Entry( self.frm_mov, textvariable = self.movet ).grid( column = 1, row = 2, columnspan = 2, sticky = EW )
        self.frm_mov.columnconfigure( 0, pad = 1 )
        self.frm_mov.columnconfigure( 2, pad = 1 )
        self.frm_mov.columnconfigure( 1, weight = 1 )
        self.movef.set( '' )
        self.movet.set( '' )

    def add_user( self, master ):
        self.frm_usr = Frame( master, bd = 1, relief = RIDGE )
        self.frm_usr.pack( side = TOP, expand = YES, fill = X )
        Label( self.frm_usr, text = 'Player' ).grid( column = 0, row = 0, columnspan = 3, sticky = EW )
        Label( self.frm_usr, text = 'Name' ).grid( column = 0, row = 1, sticky = EW )
        Label( self.frm_usr, text = 'Color' ).grid( column = 1, row = 1, sticky = EW )
        Label( self.frm_usr, text = 'xxx' ).grid( column = 2, row = 1, sticky = EW )
        self.frm_usr_list_name = Listbox( self.frm_usr, height = 4, width = 11 )
        self.frm_usr_list_name.insert( END, 'Here' )
        self.frm_usr_list_name.insert( END, 'is' )
        self.frm_usr_list_name.insert( END, 'my' )
        self.frm_usr_list_name.insert( END, 'name' )
        self.frm_usr_list_name.grid( column = 0, row = 2, sticky = NS )
        self.frm_usr_list_color = Listbox( self.frm_usr, height = 4, width = 7 )
        self.frm_usr_list_color.insert( END, 'Here' )
        self.frm_usr_list_color.insert( END, 'is' )
        self.frm_usr_list_color.insert( END, 'your' )
        self.frm_usr_list_color.insert( END, 'color' )
        self.frm_usr_list_color.grid( column = 1, row = 2 , sticky = NS )
        self.frm_usr_list_xxx = Listbox( self.frm_usr, height = 4 )
        self.frm_usr_list_xxx.insert( END, 'Here' )
        self.frm_usr_list_xxx.insert( END, 'is' )
        self.frm_usr_list_xxx.insert( END, 'the' )
        self.frm_usr_list_xxx.insert( END, 'comment' )
        self.frm_usr_list_xxx.grid( column = 2, row = 2, sticky = NSEW )
        self.frm_usr.columnconfigure( 0, pad = 1 )
        self.frm_usr.columnconfigure( 1, pad = 1 )
        self.frm_usr.columnconfigure( 2, weight = 1 )

    def add_log( self, master ):
        self.frm_log = Frame( master , bd = 1, relief = RIDGE )
        self.frm_log.pack( side = TOP, expand = YES, fill = X )
        Label( self.frm_log, text = 'Logs' ).grid( column = 0, row = 0, columnspan = 2, sticky = EW )
        self.frm_log_listbox = Listbox( self.frm_log, bg = 'white', height = 8 )
        self.frm_log_sbar = Scrollbar( self.frm_log )
        self.frm_log_sbar.grid( column = 1, row = 1, sticky = NS )
        self.frm_log_sbar.config( command = self.frm_log_listbox.yview() )
        self.frm_log_listbox.config( yscrollcommand = self.frm_log_sbar.set )
        self.frm_log_listbox.grid( column = 0, row = 1, sticky = NSEW )
        self.frm_log.columnconfigure( 0, weight = 1 )
        self.frm_log.columnconfigure( 1, pad = 1 )

    def add_msg( self , master ):
        self.frm_msg = Frame( master, bd = 1, relief = RIDGE )
        self.frm_msg.pack( side = TOP, expand = YES, fill = X )
        Label( self.frm_msg, text = 'Message' ).grid( column = 0, row = 0, columnspan = 3, sticky = EW )
        Label( self.frm_msg, text = 'Enter new:' ).grid( column = 0, row = 2, sticky = W )
        self.frm_msg_text = Text( self.frm_msg, bg = 'white', height = 8, width = 16 )
        self.frm_msg_text.grid( row = 1, column = 0, columnspan = 2, sticky = NSEW )
        self.frm_msg_sbar = Scrollbar( self.frm_msg )
        self.frm_msg_sbar.grid( row = 1, column = 2, sticky = NS )
        self.frm_msg_sbar.config( command = self.frm_msg_text.yview )
        self.frm_msg_text.config( yscrollcommand = self.frm_msg_sbar.set )
        msg = StringVar()
        msg.set( '' )
        ent = Entry( self.frm_msg, textvariable = msg, bg = 'white' )
        ent.grid( column = 1, row = 2, columnspan = 2, sticky = EW )
        self.frm_msg.columnconfigure( 0, pad = 1 )
        self.frm_msg.columnconfigure( 1, weight = 1 )
        self.frm_msg.columnconfigure( 2, pad = 1 )

    def add_board( self ):
        self.board = Board( self , relief = GROOVE, bd = 1, padx = 1, pady = 1, bg = 'white' )
        self.board.grid( column = 0, row = 0, sticky = NSEW )
        self.board.SetClient( self.client )
        self.board.Draw_Background()
        self.board.config( height = 800, width = 800 )

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
                showerror( 'Error' , 'Connection not created, \nView logs for more detail' )
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
        ent1.bind( ' < Return > ', jump )
        ent2.bind( ' < Return > ', fetch )
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
                self.event_generate( ' << name >> ' )
            else:
                showerror( 'Error', 'Name should not be empty' )
                name.set( self.client.prof.name )
                return
            if id.get() in range( define.MAXPLAYER ):
                self.client.prof.id = int( id.get() )
                id.set( self.client.prof.id )
                self.event_generate( ' << id >> ' )
            else:
                showerror( 'Error', 'Id should be in 0..3' )
                return
            try:
                exp.config( bg = color.get() )
                self.client.prof.bg = color.get()
                self.event_generate( ' << color >> ' )
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
                    self.event_generate( ' << color >> ' )
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
        e1.bind( ' < Return > ', ( lambda : fetch( True ) ) )
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
    c = client.Client()
    c.run()
