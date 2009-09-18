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
import queue
import time
try:
    #Python 2.x
    import thread
except:
    #Python 3.x
    import _thread as thread

import define
from profile import Profile
from clientGUI import clientGUI, Startup
from message import MsgSocket
from definemsg import *

class Client():

    def __init__( self ):
        self.input = sys.stdin
        self.output = sys.stdout
        self.map = define.CheckerBoard()
        self.queue = queue.Queue()
        self.socket = None
        self.lock = thread.allocate_lock()
        self.init()

    def init( self ):
        self.stat = define.CLI_INIT
        filename = Startup()
        if filename == None:
            sys.exit()
        if define.log_lv & define.LOG_DEF:
            print( filename )
        name = filename.split( '/' )[-1].split( '\\' )[-1].rsplit( '.' )[0]
        if define.log_lv & define.LOG_DEF:
            print( 'username :', name )
        self.prof = Profile( name )
        self.prof.load()
        self.map.Dump( self.prof.lineup, self.prof.id * define.MAXCHESS )
        self.gui = clientGUI( self )

    def consumer( self, msec = 1000 ):
        try:
            data = self.queue.get( block = False )
        except queue.Empty:
            pass
        else:
            if define.log_lv & define.LOG_QUE:
                print( data )
            #nothing to do....currently
        self.gui.after( msec, self.consumer )

    def run( self ):
        self.consumer()
        self.gui.run()
        try:
            self.Connection_Close()
        except Exception as e:
            if define.log_lv & define.LOG_MSG:
                print( str( e ) )

        self.prof.save()
        sys.stdin = self.input
        sys.stoud = self.output
        #sys.exit()

    def Connection_Create( self, host = None, port = None ):
        if not self.socket:
            if ( host == None ) | ( port == None ):
                host = self.prof.host
                port = self.prof.port
            self.socket = MsgSocket()
            try:
                self.socket.connect( ( host, port ) )
            except Exception as e:
                if define.log_lv & define.LOG_MSG:
                    print( e )
                self.socket = None
            return self.Connection_Init()

    def Connection_Init( self ):
        try:
            while True:
                cmd, arg = self.socket.recv_split()
                if cmd == CMD_ERROR:
                    raise Exception( arg )
                elif cmd == CMD_COMMENT:
                    if define.log_lv & define.LOG_MSG:
                        print( arg )
                elif cmd == CMD_ASK:
                    if arg == FIL_ID:
                        self.socket.send_join( CMD_TELL, 'int', ( FIL_ID, self.prof.id ) )
                    elif arg == FIL_NAME:
                        self.socket.send_join( CMD_TELL, 'str', ( FIL_NAME, self.prof.name ) )
                    elif arg == FIL_LINEUP:
                        self.socket.send_join( CMD_TELL, 'str', ( FIL_LINEUP, self.prof.lineup.toStr() ) )
                elif cmd == CMD_WAIT:
                    break
        except Exception as e:
            if define.log_lv & define.LOG_MSG:
                print( e )
            self.socket = None
        else:
            self.status = define.CLI_WAIT
            self.thread = thread.start_new( self.Connection_Run, () )

    def Connection_Run( self ):
        while True:
            self.lock.acquire()
            if self.socket == None:
                self.lock.release()
                break
            self.socket.send_join( CMD_ASK, 'str', 'move' )
            print( 'READING answer' )
            cmd, arg = self.socket.recv_split()
            self.lock.release()
            if cmd == CMD_ERROR:
                raise Exception( arg )
            elif cmd == CMD_COMMENT:
                if define.log_lv & define.LOG_MSG:
                    print( arg )
            elif cmd == CMD_TELL:
                filter, arg = arg[0], arg[1]
                if filter == FIL_MOVE:
                    fpos, tpos = arg[0], arg[1]
                    #todo: move step
            elif cmd == CMD_MOVE:
                self.stat = define.CLI_MOVE
                #todo: get user's move
                self.stat = define.CLI_WAIT
            time.sleep( 1 )

    def Connection_Close( self ):
        if self.socket:
            self.lock.acquire()
            try:
                self.socket.send_join( CMD_EXIT, 'int', self.prof.id )
            except Exception as e:
                if define.log_lv & define.LOG_MSG:
                    print( e )
            try:
                self.socket.recv_split()
                self.socket.close()
            except Exception as e:
                if define.log_lv & define.LOG_MSG:
                    print( e )
            self.socket = None
            self.stat = define.CLI_INIT
            self.lock.release()

    def OnChangeId( self ):
        self.map.RemoveAll()
        self.prof.loadlineup()
        self.map.Dump( self.prof.lineup, self.prof.id * define.MAXCHESS )

    def test( self ):
        return

if __name__ == '__main__':
    c = Client()
    c.run()
