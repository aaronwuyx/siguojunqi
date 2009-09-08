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
import sys

import socket
#import queue
#import time
#import thread

import define
from profile import Profile
from clientGUI import clientGUI, Startup

CLI_INIT = 'init'
CLI_MOVE = 'move'
CLI_WAIT = 'wait'

class Client():

    def __init__( self ):
        self.stat = CLI_INIT
        filename = Startup()
        if filename == None:
            sys.exit()
        name = filename.split( '/' )[-1].split( '\\' )[-1].rsplit( '.' )[0]
        if define.DEBUG:
            print( 'username :', name )
        name = 'sean' #Test only
        self.map = define.CheckerBoard()
        self.prof = Profile( name )
        self.prof.load()
        self.socket = None
        self.socketbufsize = 1024
        self.gui = clientGUI( self )

    def run( self ):
        self.gui.mainloop()
        if self.socket:
            try:
                self.Connection_Close()
            except Exception as e:
                if define.DEBUG:
                    print( str( e ) )
        self.prof.save()

    def test( self ):
        if not self.socket:
            return
        while True:
            data = input( '> ' )
            if not data:
                break
            data += os.linesep
            self.socket.send( data.encode( 'utf8' ) )
            data = self.socket.recv( self.socketbufsize )
            if not data:
                break
            print( data.strip() )

    def Connection_Create( self ):
        if self.socket == None:
            self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            try:
                self.socket.connect( ( self.prof.host, self.prof.port ) )
                self.status = CLI_WAIT
            except Exception as e:
                if define.DEBUG:
                    print( str( e ) )
                self.socket = None

    def Connection_Close( self ):
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                if define.DEBUG:
                    print( str( e ) )
            self.socket = None
            self.status = CLI_INIT


"""
    def createConnection( self ):
            Sendline( self.socket, Combline( CMD_ADD, 'int', self.conf.player ) )
            data, self.remain = Recvline( self.socket, self.remain )
            cmd, arg, obj = Sepline( data )
            if cmd == 'error':
                raise Exception( str( obj ) )

    def closeConnection( self ):
            #inform server
            try:
                Sendline( self.socket, Combline( CMD_EXIT, 'int', self.conf.player ) )
            except Exception:
                pass
"""
if __name__ == '__main__':
    c = Client()
    c.run()
