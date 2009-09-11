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

#import queue
#import time
#import thread

import define
from profile import Profile
from clientGUI import clientGUI, Startup
from message import MsgSocket
from definemsg import *

class Client():

    def __init__( self ):
        self.map = define.CheckerBoard()
        self.socket = None
        self.init()

    def init( self ):
        self.stat = define.CLI_INIT
        filename = Startup()
        if filename == None:
            sys.exit()
        if define.DEBUG:
            print( filename )
        name = filename.split( '/' )[-1].split( '\\' )[-1].rsplit( '.' )[0]
        if define.DEBUG:
            print( 'username :', name )
        self.prof = Profile( name )
        self.prof.load()
        self.gui = clientGUI( self )

    def run( self ):
        self.gui.mainloop()
        try:
            self.Connection_Close()
        except Exception as e:
            if define.DEBUG:
                print( str( e ) )

        self.prof.save()
        #sys.exit()

    def Connection_Create( self, host = None, port = None ):
        if self.socket == None:
            if ( host == None ) | ( port == None ):
                host = self.prof.host
                port = self.prof.port
            self.socket = MsgSocket()
            try:
                self.socket.connect( ( host, port ) )
                self.socket.send_join( CMD_ID, 'int', self.prof.id )
                cmd, arg = self.socket.recv_split()
                if cmd == CMD_ERROR:
                    self.socket.close()
                    raise Exception( 'arg' )
                self.status = define.CLI_WAIT
                #self.thread = start_new( Connection_Treat, () )
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
            self.status = define.CLI_INIT

    def test( self ):
        return

"""
    def createConnection( self ):
            Sendline( self.socket, Combline( CMD_ADD, 'int', self.conf.player ) )
            data, self.remain = Recvline( self.socket, self.remain )
            cmd, arg, obj = Sepline( data )
            if cmd == 'error':
                raise Exception( str( obj ) )

    def closeConnection( self ):
            try:
                Sendline( self.socket, Combline( CMD_EXIT, 'int', self.conf.player ) )
            except Exception:
                pass
"""

if __name__ == '__main__':
    c = Client()
    c.run()
