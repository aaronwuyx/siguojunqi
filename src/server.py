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
        self.locks = []
        for i in range( define.MAXPLAYER ):
            self.clients.append( None )
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
        conn = MsgMixin( connection )
        while True:
            cmd, id = conn.recv_split()
            if cmd == CMD_COMMENT:
                continue
            elif cmd == CMD_ID:
                break
            else:
                conn.send_join( CMD_ERROR, 'str', 'send id at first' )
                conn.close()
                return
        if ( id >= define.MAXPLAYER ) | ( id < 0 ):
            conn.send_join( CMD_ERROR, 'str', 'invalid id number' )
            conn.close()
            return
        if self.clients[id]:
            conn.send_join( CMD_ERROR, 'str', 'duplicate id number' )
            conn.close()
            return

        self.clients[id] = conn
        self.clientcount += 1
        return id

    def client_run( self, id ):
        self.clients[id].send_join( CMD_ASK, 'str', 'name' )
        #self.clients[id].send_join( CMD_ASK, 'str', 'lineup' )
        #get lineup
        #tell others about him
        while True:
            self.locks[id].acquire()
            if self.clients[id] == None:
                break
            if self.stat == define.SRV_INIT:
                self.clients[id].send_join( CMD_WAIT, 'float', 0.5 )
            elif self.stat == define.SRV_MOVE:
                if self.onmove == id:
                    #      ask for move... verify it... tell others
                    pass
                else:
                    self.clients[id].send_join( CMD_WAIT, 'float', 0.5 )
            time.sleep( 1 )
            self.locks[id].release()
        #    if disconnecting... run client_del

    def client_del( self, id ):
        if not self.clients[id]:
            return
        self.locks[id].acquire()
        try:
            self.clients[id].socket.close()
        except Exception as e:
            if define.DEBUG:
                print( str( e ) )
        self.clients[id] = None
        self.clientcount -= 1
        self.locks[id].release()
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
        while True:
            self.tlocks[k].acquire()
            if self.status == CMD_EXIT:
                Sendline( self.client[k][0], Combline( CMD_EXIT, 'int', k + 1 ) )
            elif ( self.status == CMD_MOVE ) & ( self.onmove == k ):
                Sendline( self.client[k][0], Combline( CMD_ONMOVE, 'int', k + 1 ) )
            else:
                Sendline( self.client[k][0], Combline( CMD_WAIT, 'int', k + 1 ) )
            self.tlocks[k].release()
            time.sleep( 1 )

            self.tlocks[k].acquire()
            data, self.remain[k] = Recvline( self.client[k][0], self.remain[k] )
            if data == '':
                self.del_client( k )
                raise Exception( 'Disconnected from client unknown reason...' )
            self.tlocks[k].release()
            cmd, arg, obj = Sepline( data )

            if cmd == CMD_EXIT:
                self.del_client( k )
                break
            elif cmd == CMD_MOVE:
                fpos = obj[0]
                tpos = obj[1]
                if self.map.move( fpos, tpos ):
                    self.tell_others( k, Combline( CMD_MOVE, 'int,int', obj ) )
                    if DEBUG:
                        print( 'move from', fpos, 'to', tpos, ', Player no ', k + 1 )
                    self.onmove = ( self.onmove + 1 ) % DEFAULTPLAYER
            else:
                if DEBUG:
                    print( cmd, arg, obj )
                raise Exception( 'Unknown str ' + cmd )
"""

if __name__ == '__main__':
    s = SiGuoServer()
    s.run()
