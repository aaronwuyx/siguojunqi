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
import logging
try:
    #python 2.x
    import thread
except ImportError:
    #python 3.x
    import _thread as thread

import define
from scstat import *
from msg import MsgMixin, DEFAULTPORT
from msgdef import *

class sgserver():
    def __init__( self, port = DEFAULTPORT ):
        self.stat = SRV_INIT
        self.init_data()
        self.init_socket( port )

    def init_socket( self , port ):
        self.socket = socket.socket()
        self.socket.bind( ( 'localhost', port ) )
        self.socket.listen( 4 ) #at most 4 players
        self.stat = SRV_DISCONNECTED

    def init_data( self ):
        if self.stat != SRV_DISCONNECTED and self.stat != SRV_INIT:
            return - 1
        self.map = define.CheckerBoard()
        self.onmove = random.choice( range( 0, define.MAXPLAYER ) )

        #client info
        self.cli_num = 0
        self.cli = []
        self.cli_addr = []
        self.cli_name = []
        self.cli_alive = []
        self.cli_locks = []
        for i in range( define.MAXPLAYER ):
            self.cli.append( None )
            self.cli_name.append( '' )
            self.cli_addr.append( None )
            self.cli_alive.append( False )
            t = thread.allocate_lock()
            self.cli_locks.append( t )
        self.board_lock = thread.allocate_lock()

    def run( self ):
        if self.stat != SRV_INIT:
            return - 1
        onRun = True
        while onRun:
            try:
                err = self.get4cli()
                if err:
                    exit( 1 )
                self.stat = SRV_MOVE1
                err = self.game_run()
                if err:
                    exit( 1 )
                self.stat = SRV_QUIT
                err = self.game_quit()
                if err:
                    exit( 1 )
                self.stat = SRV_DISCONNECTED
                err = self.init_data()
                if err:
                    exit( 1 )
            except KeyboardInterrupt, SystemExit:
                onRun = False

    def quit( self ):
        self.socket.close()

    def get4cli( self ):
        if self.stat != SRV_DISCONNECTED:
            return - 1
        while True:
            ( cli_socket, addr ) = self.socket.accept()
            logging.debug( 'Connection from address ' + str( addr ) )
            id = self.cli_add( cli_socket, addr )
            if id == None or id >= define.MAXPLAYER or id < 0:
                continue
            thread.start_new( self.cli_run, ( id , ) )
            if self.cli_num == define.MAXPLAYER:
                break

    def game_run( self ):
        pass

    def game_quit( self ):
        if self.stat != SRV_QUIT:
            return - 1
        #send steps, request connection close
        self.INFORM_ALL( CMD_EXIT )
        while self.cli_num > 0:
           time.sleep( 0.5 )

    def cli_add( self, connection, addr ):
        '''
        check client's id, verify it, then add client into list self.clients,
        in this version, add MsgMixin into self.clients
        return value: client id, or None if it is invalid
        '''

        self.stat = SRV_CONNECTING
        conn = MsgMixin( connection )
        #suppose we will recv "id, name, lineup"
        #conn.send_join( CMD_ASK, 'sss',('id','name','lineup') )
        cmd, typ, arg = conn.recv_split()
        if cmd == CMD_INFORM:
            try:
                id, name, lineup = arg[0], arg[1], arg[2]
            except IndexError:
                conn.close()
                return
            except ValueError:
                conn.close()
                return
            except TypeError:
                conn.close()
                return
        else:
            conn.close()
            return
        if id >= define.MAXPLAYER or id < 0:
            logging.error( 'invalid id number' )
            conn.close()
            return
        if not name:
            logging.error( 'no name specified' )
            conn.close()
            return
        self.board_lock.acquire()
        if self.cli[id]:
            self.board_lock.release()
            logging.error( 'duplicated id number' )
            conn.close()
            return
        self.cli[id] = conn
        self.cli_addr[id] = addr
        self.cli_name[id] = name
        self.cli_alive[id] = True
        self.cli_num = self.cli_num + 1
        self.map.Copy_From_Lineup( id, lineup )
        self.board_lock.release()
        logging.debug( 'id :' + str( id ) + ' name :' + name )
        #tell new player to add others
        self.board_lock.acquire()
        for cid in range( define.MAXPLAYER ):
            if cid != id and self.cli[cid]:
                self.cli[id].send_add( CMD_INFORM, 'sis', ( PLY_ADD, cid, self.cli_name[cid] ) )
        self.board_lock.release()

        #tell others to add the new player
        self.INFORM_ALL( CMD_INFORM, 'sis' , ( PLY_ADD, id, name ) )
        self.stat = SRV_DISCONNECTED
        return id

    def INFORM_ALL( self , cmd, typ, arg ):
        pass

class SiGuoServer():
    def IsAlive( self, id ):
        pass
        '''
        first, check if its 32 is alive,
        then the client can move...
        '''

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
    s = sgserver()
    s.run()
    s.quit()
