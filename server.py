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
    def __init__( self, Port = define.DEFAULTPORT ):
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
        self.alive = []
        for i in range( define.MAXPLAYER ):
            self.alive.append( False )
            self.clients.append( None )
            self.names.append( None )
            self.locks.append( thread.allocate_lock() )

    def run( self ):
        while True:
            ( clientsocket, address ) = self.socket.accept()
            if define.log_lv & define.LOG_DEF:
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

    def IsAlive( self, id ):
        pass
        '''
        first, check if its 32 is alive,
        then the client can move...
        '''

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
        conn.send_join( CMD_ASK, 'str', FIL_ID )
        while True:
            cmd, arg = conn.recv_split()
            print( cmd, arg )
            if cmd == CMD_TELL:
                if arg[0] != FIL_ID:
                    continue
                if ( arg[1] >= define.MAXPLAYER ) | ( arg[1] < 0 ):
                    conn.send_join( CMD_ERROR, 'str', 'invalid id number' )
                    conn.socket.close()
                    return
                if self.clients[arg[1]]:
                    conn.send_join( CMD_ERROR, 'str', 'duplicate id number' )
                    conn.socket.close()
                    return
                id = arg[1]
                break
            elif cmd == CMD_COMMENT:
                if define.log_lv & define.LOG_MSG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()
        if define.log_lv & define.LOG_DEF:
            print( 'id = ', id )

        conn.send_join( CMD_ASK, 'str', FIL_NAME )
        while True:
            cmd, arg = conn.recv_split()
            if cmd == CMD_TELL:
                if arg[0] != FIL_NAME:
                    continue
                name = arg[1]
                break
            elif cmd == CMD_COMMENT:
                if define.log_lv & define.LOG_MSG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()
        if define.log_lv & define.LOG_DEF:
            print( 'name = ', name )

        conn.send_join( CMD_ASK, 'str', FIL_LINEUP )
        while True:
            cmd, arg = conn.recv_split()
            if cmd == CMD_TELL:
                if arg[0] != FIL_LINEUP:
                    continue
                lineupstr = arg[1]
                lineup = define.Lineup( id )
                try:
                    lineup.fromStr( lineupstr )
                except Exception:
                    conn.send_join( CMD_ERROR, 'str', 'invalid lineup' )
                    conn.close()
                    return
                break
            elif cmd == CMD_COMMENT:
                if define.log_lv & define.LOG_MSG:
                    print( arg )
                continue
            elif cmd == CMD_EXIT:
                conn.close()

        self.clients[id] = conn
        self.names[id] = name
        self.alive[id] = True
        self.map.Dump( lineup, id * define.MAXCHESS )

        self.gamelock.acquire()
        self.clientcount += 1
        if define.log_lv & define.LOG_DEF:
            print( 'clientnum = ', self.clientcount )
        #tell others about him
        self.gamelock.release()
        conn.send_join( CMD_WAIT, 'int', 1 )
        self.tell_all( CMD_TELL, ( 'str', 'int', 'str' ), ( FIL_IDNAME, id, name ) )
        for count in range( define.MAXPLAYER ):
            if count == id:
                continue
            if self.clients[count]:
                self.clients[id].send_add( CMD_TELL, ( 'str', 'int', 'str' ), ( FIL_IDNAME, count, self.names[count] ) )
        return id

    def client_run( self, id ):
        while self.clients[id]:
            self.locks[id].acquire()
            cmd, arg = self.clients[id].recv_split()
            self.locks[id].release()
            if cmd == CMD_COMMENT:
                if define.log_lv & define.LOG_MSG:
                    print( arg )
                continue
            elif cmd == CMD_ASK:
                self.locks[id].acquire()
                if self.stat == define.SRV_INIT:
                    self.clients[id].send_join( CMD_WAIT, ['int'], [1] )
                elif self.stat == define.SRV_MOVE:
                    if self.onmove == id:
                        self.clients[id].send_join( CMD_ASK, 'str', FIL_MOVE )
                    else:
                        self.clients[id].send_join( CMD_WAIT, ['int'], [1] )
                self.locks[id].release()
            elif cmd == CMD_TELL:
                self.locks[id].acquire()
                if arg[0] == FIL_MOVE:
                    if self.onmove == id:
                        source = arg[1]
                        target = arg[2]
                        if self.map.CanMove( source, target ):
                            result = self.map.Result( source, target )
                            self.map.Move( source, target, result )
                            self.tell_all( CMD_TELL, ( 'str', 'int', 'int', 'int' ), ( FIL_MOVE2, source, target, result ) )
                            for i in range( define.MAXPLAYER ):
                                if self.alive[id]:
                                    if IsAlive( id ):
                                        pass
                                    else:
                                        self.OneLose( id )
                            self.onmove = ( self.onmove + 1 ) % define.MAXPLAYER
                            while not self.alive[self.onmove]:
                                self.onmove = ( self.onmove + 1 ) % define.MAXPLAYER
                        else:
                            #some bug here?
                            if define.log_lv & define.LOG_MSG:
                                print( 'Move: from ', source, 'to', target )
                            self.clients[id].send_join( CMD_ASK, 'str', FIL_MOVE )
                self.clients[id].send_join( CMD_WAIT, ['int'], [1] )
                self.locks[id].release()
            elif cmd == CMD_EXIT:
                self.client_del( id )
            time.sleep( 1 )

    def OneLose( self, id ):
        self.gamelock.acquire()
        for pos in self.map.size():
            if self.map.item[pos].IsChess():
                if self.map.item[pos].GetChess().GetPlayer() == id:
                    self.map.Remove( pos )
        self.alive[id] = False
        self.tell_all( CMD_TELL, ['str', 'int'], [FIL_LOSE, id] )
        self.gamelock.release()

    def client_del( self, id ):
        if not self.clients[id]:
            return
        self.locks[id].acquire()
        try:
            self.clients[id].send_join( CMD_EXIT, 'int', id )
            self.clients[id].socket.close()
        except socket.error as e:
            if define.log_lv & define.LOG_MSG:
                print( e )
        self.clients[id] = None
        self.names[id] = None
        self.locks[id].release()
        self.DestroyAll( id )

        self.gamelock.acquire()
        self.clientcount -= 1
        for pos in self.map.size:
            if self.map.item[pos].IsChess():
                if self.map.item[pos].GetChess().GetPlayer() == id:
                    self.map.Remove( pos )
        self.gamelock.release()
        if define.log_lv & define.LOG_DEF:
            print( 'connection close, id = ', id )
        thread.exit()

    def tell_all( self, cmd, typ, arg ):
        self.gamelock.acquire()
        for id in range( define.MAXPLAYER ):
            if self.clients[id]:
                #need buffer in message send
                self.clients[id].send_add( cmd, typ, arg )
        self.gamelock.release()

if __name__ == '__main__':
    s = SiGuoServer()
    s.run()