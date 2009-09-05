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

import socket
import os
import sys
import time
import thread

from define import CheckerBoard, Chess, Lineup
from profile import Profile
from message import *
from clientGUI import *

CLI_INIT = 'init'
CLI_MOVE = 'move'
CLI_WAIT = 'wait'

class Client():

    def __init__( self ):
        self.stat = CLI_INIT
        name, id, graphic = Startup()
        self.map = CheckerBoard()
        self.prof = Profile( '' )
        self.prof.load()

        rule.PlaceOne( self.conf.place, self.map, self.conf.player )

        self.guiopt = thread.allocate_lock()
        self.top = None
        self.menus = {}
        self.toolbutton = []

        self.socket = None
        self.remain = ''

    def run( self ):
        self.make_gui()
        self.top.mainloop()

        self.closeConnection()
        self.conf.Save( 'default.cfg' )

    def closeConnection( self ):
        if self.socket != None:
            #inform server
            try:
                Sendline( self.socket, Combline( CMD_EXIT, 'int', self.conf.player ) )
            except Exception:
                pass
            #try to close connection anyway
            try:
                self.socket.close()
            except Exception:
                pass

            self.socket = None
            self.status = CLIENT_INIT
            return True
        return False

    def createConnection( self ):
        if self.socket == None:
            self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.socket.connect( ( self.conf.host, self.conf.port ) )
            Sendline( self.socket, Combline( CMD_ADD, 'int', self.conf.player ) )
            data, self.remain = Recvline( self.socket, self.remain )
            cmd, arg, obj = Sepline( data )
            if cmd == 'error':
                raise Exception( str( obj ) )
            self.status = CLIENT_START

if __name__ == '__main__':
    c = Client()
    c.run()
