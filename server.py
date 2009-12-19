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
        self.steps = []

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

    def game_over( self ):
        """ 
        return 0 - game_over
        return 1 - 1P 0,3P 2 wins
        return 2 - 2P 1,4P 3 wins
        return 3 - nobody wins
        """
        self.board_lock.acquire()
        a = not self.cli_alive[0] and not self.cli_alive[2]
        b = not self.cli_alive[1] and not self.cli_alive[3]
        self.board_lock.release()
        if a and b:
            return 3
        elif a:
            return 2
        elif b:
            return 1
        else:
            return 0

    def game_run( self ):
        self.stat = SRV_MOVE1
        laststep = 0
        while self.game_over() == 0:
            if len( self.steps ) != laststep:
                laststep = len( self.steps )
                self.onmove = ( self.onmove + 1 ) % define.MAXPLAYER
                while self.game_over() == 0 and not self.cli_alive[self.onmove]:
                    self.onmove += 1
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
        self.cli_locks[id].acquire()
        for cid in range( define.MAXPLAYER ):
            if cid != id and self.cli[cid]:
                self.cli[id].send_add( CMD_INFORM, 'sis', ( PLY_ADD, cid, self.cli_name[cid] ) )
        self.cli_locks[id].release()

        #tell others to add the new player
        self.INFORM_ALL( CMD_INFORM, 'sis' , ( PLY_ADD, id, name ) )
        self.stat = SRV_DISCONNECTED
        return id

    def INFORM_ALL( self , cmd, typ, arg ):
        for id in range( define.MAXPLAYER ):
            self.cli_locks[id].acquire()
            self.cli[id].send_add( cmd, typ, arg )
            self.cli_locks[id].release()

    def cli_run( self, id ):
        while self.cli[id]:
            cmd, typ, arg = self.cli[id].recv_split()
            if cmd == CMD_ERROR:
                continue
            elif cmd == CMD_ASK:
                if typ == 'i':
                    p = arg[0]
                    if p > len( self.steps ):
                        self.cli_locks[id].acquire()
                        self.cli[id].send_add( CMD_ERROR, 's', ( 'invalid step number', ) )
                        self.cli_locks[id].release()
                    else:
                        self.cli_locks[id].acquire()
                        self.cli[id].send_add( CMD_REPLY, '2', ( self.steps[p], ) )
                        self.cli_locks[id].release()
            elif cmd == CMD_INFORM:
                if typ == '1':
                    self.board_lock.acquire()
                    #check the step, who moves, and the step numbers is the current one
                    step = arg[0]
                    if self.onmove == id and step.num == len( self.steps ):
                        if self.map.CanMove( step.fpos, step.tpos ):
                            result = self.map.Result( step.fpos, step.tpos )
                            self.map.Move( step.fpos, step.tpos, result )
                            step2 = Move2( len( self.steps ), step.fpos, step.tpos, result )
                            self.steps.append( step2 )
                            #do not use INFORM_ALL here, wait for clients to ask for new steps by sending CMD_ASK
                            #self.INFORM_ALL( cmd_INFORM, '2', step2 )
                        else:
                            #do not return errors,either. let te client to check if he continues to move
                            #this situation was not supposed to happen, if only there are network problems...
                            pass

                    self.board_lock.release()
            elif cmd == CMD_EXIT:
                self.cli_rem( id )

    def cli_rem( self, id ):
        #tell others to remove the new player
        self.INFORM_ALL( CMD_INFORM, 'sis' , ( PLY_REM, id, name ) )

        self.board_lock.acquire()
        self.cli[id] = None
        self.cli_addr[id] = None
        self.cli_name[id] = None
        self.cli_alive[id] = None
        self.cli_num = self.cli_num - 1
        self.board.lock.release()

class SiGuoServer():

    def client_run( self, id ):
            if cmd == CMD_ASK:
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
