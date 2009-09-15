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
import random
import time
try:
    #python 2.x
    import thread
except ImportError:
    #python 3.x
    import _thread as thread

import define
from message import MsgMixin
from definemsg import *

class SiGuoServer():
    def __init__( self, Port = define.DEFAULTSERVERPORT ):
        self.socket = socket.socket()
        self.socket.bind( ( 'localhost', Port ) )
        self.socket.listen( 4 )
        self.init()

    def init( self ):
        self.map = define.CheckerBoard()
        self.stat = define.SRV_INIT
        self.onmove = random.choice( range( 0, define.MAXPLAYER ) )

        #client info & locks
        self.clientcount = 0
        self.gamelock = thread.allocate_lock()

        self.clients = []
        self.names = []
        self.locks = []
        for i in range( define.MAXPLAYER ):
            self.clients.append( None )
            self.names.append( None )
            self.locks.append( thread.allocate_lock() )

    def run( self ):
        while True:
            ( clientsocket, address ) = self.socket.accept()
            if define.DEBUG:
                print( 'Connection from address ', address )
            id = self.client_add( clientsocket, address )
            if id == None:
                continue
            thread.start_new( self.client_run, ( id, ) )
            if self.clientcount == define.MAXPLAYER:
                break

        self.stat = define.SRV_MOVE
        while self.clientcount > 0:
            time.sleep( 1 )
        self.socket.close()

    '''
        check client's id, verify it, then add client into list self.clients,
        in this version, add MsgMixin into self.clients
        return value: client id, or None if it is invalid
    '''
    def client_add( self, connection, addr ):
        id = None
        Name = None
        lineup = None
        conn = MsgMixin( connection )
        conn.send_join( CMD_ASK, 'str', 'id' )
        while True:
            cmd, arg = conn.recv_split()
            print( cmd, arg )
            if cmd == CMD_TELL:
                if ( arg >= define.MAXPLAYER ) | ( arg < 0 ):
                    conn.send_join( CMD_ERROR, 'str', 'invalid id number' )
                    conn.close()
                    return
                if self.clients[arg]:
                    conn.send_join( CMD_ERROR, 'str', 'duplicate id number' )
                    conn.close()
                    return
                id = arg
                break
            elif cmd == CMD_COMMENT:
                if define.DEBUG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()
        if define.DEBUG:
            print( 'id = ', id )
        conn.send_join( CMD_ASK, 'str', 'name' )
        while True:
            cmd, arg = conn.recv_split()
            if cmd == CMD_TELL:
                name = arg
                break
            elif cmd == CMD_COMMENT:
                if define.DEBUG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()
        if define.DEBUG:
            print( 'name = ', name )
        conn.send_join( CMD_ASK, 'str', 'lineup' )
        while True:
            cmd, arg = conn.recv_split()
            if cmd == CMD_TELL:
                lineup = arg
                break
            elif cmd == CMD_COMMENT:
                if define.DEBUG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()

        self.clients[id] = conn
        self.names[id] = name
        #self.map.xxx(lineup)
        self.gamelock.acquire()
        self.clientcount += 1
        if define.DEBUG:
            print( 'clientnum = ', self.clientcount )
        #tell others about him
        self.gamelock.release()
        conn.send_join( CMD_WAIT, 'int', 1 )
        return id

    def client_run( self, id ):
        while self.clients[id]:
            print( 'Reading socket...' )
            cmd, arg = self.clients[id].recv_split()
            if cmd == CMD_COMMENT:
                if define.DEBUG:
                    print( arg )
                continue
            elif cmd == CMD_ASK:
                if self.stat == define.SRV_INIT:
                    self.clients[id].send_join( CMD_WAIT, 'int', 1 )
                elif self.stat == define.SRV_MOVE:
                    if self.onmove == id:
                        self.clients[id].send_join( CMD_ASK, 'str', 'move' )
                    else:
                        self.clients[id].send_join( CMD_WAIT, 'int', 1 )
            elif cmd == CMD_TELL:
                if self.onmove == id:
                    #verify move, move, tell all players
                    pass
            elif cmd == CMD_EXIT:
                self.client_del( id )
            time.sleep( 1 )

    def client_del( self, id ):
        if not self.clients[id]:
            return
        try:
            self.clients[id].close()
        except Exception as e:
            if define.DEBUG:
                print( str( e ) )
        self.locks[id].acquire()
        self.clients[id] = None
        self.locks[id].release()
        self.gamelock.acquire()
        self.clientcount -= 1
        self.gamelock.release()
        if define.DEBUG:
            print( 'connection close, id = ', id )

"""
            rule.placeone( obj, self.map, player )
            self.tell_others( k, Combline( 'placeother', 'int', player ) )

    def tell_others( self, k, targetstr ):
        for i in range( 0, DEFAULTPLAYER ):
            if i != k:
                pass
        return

    def run_client( self, k ):
            elif cmd == CMD_MOVE:
                fpos = obj[0]
                tpos = obj[1]
                if self.map.move( fpos, tpos ):
                    self.tell_others( k, Combline( CMD_MOVE, 'int,int', obj ) )
                    if DEBUG:
                        print( 'move from', fpos, 'to', tpos, ', Player no ', k + 1 )
                    self.onmove = ( self.onmove + 1 ) % DEFAULTPLAYER
"""

if __name__ == '__main__':
    s = SiGuoServer()
    s.run()
