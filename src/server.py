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
import socketserver
import random
import time

import define

class EchoRequestHandler( socketserver.StreamRequestHandler ):
    def handle( self ):
        print( 'Connection from: ', self.client_address )
        data = self.rfile.readline().decode()
        self.wfile.write( data.encode( 'utf8' ) )
        self.server.serve_forever()

class SiGuoServer:
    def __init__( self, URL = define.DEFAULTSERVERURL, Port = define.DEFAULTSERVERPORT ):
        self.server = socketserver.TCPServer( ( URL, Port ), EchoRequestHandler )

    def run( self ):
        self.server.serve_forever()

"""
class SiGuoServer:
    def __init__( self, URL = 'localhost', Port = 30000 ):
        self.map = rule.Map( len( Pos4 ) )
        self.status = CMD_WAIT #status
        self.extra = None #indicate who move/exit/wait
        #create socket
        self.socket = socket( AF_INET, SOCK_STREAM )
        self.socket.bind( ( URL, Port ) )
        self.socket.listen( 5 )
        #client info & locks
        self.clientcount = 0
        self.client = []
        self.remain = []
        self.tlocks = []
        for i in range( DEFAULTPLAYER ):
            self.client.append( None )
            self.remain.append( None )
            #one lock per thread ... r/w message
            self.tlocks.append( thread.allocate_lock() )
        self.clientlock = thread.allocate_lock()
        self.mainlock = thread.allocate_lock()

    def add_client( self ):
        conn, addr = self.socket.accept()
        if DEBUG:
            print( 'connection from address ', addr )
        data, remain = Recvline( conn, '' )
        cmd, arg, player = Sepline( data )
        if ( cmd != CMD_ADD ) or ( arg != 'int' ) or ( player <= 0 ) or ( player > DEFAULTPLAYER ):
            Sendline( conn, Combline( CMD_ERROR, 'string', 'invalid player number' ) )
            conn.close()
            return False
        self.clientlock.acquire()
        k = player - 1
        if self.client[k]:
            Sendline( conn, Combline( CMD_ERROR, 'string', 'duplicate player number' ) )
            self.clientlock.release()
            conn.close()
            return False
        self.client[k] = ( conn, addr )
        self.remain[k] = remain
        self.clientcount += 1
        self.clientlock.release()
        if DEBUG:
            print( ' player no ', player )
        self.tlocks[k].acquire()
        Sendline( conn, Combline( CMD_PLACE, 'int', k ) )
        data, self.remain[k] = Recvline( self.client[k][0], self.remain[k] )
        cmd, arg, obj = Sepline( data )
        while cmd != CMD_PLACE:
            data, self.remain[k] = Recvline( self.client[k][0], self.remain[k] )
            if data == '':
                break
            cmd, arg, obj = Sepline( data )
        self.tlocks[k].release()
        if data == '':
            #disconnected somehow
            self.del_client( k )
        else:
            rule.placeone( obj, self.map, player )
            self.tell_others( k, Combline( 'placeother', 'int', player ) )
        return k

    def tell_others( self, k, targetstr ):
        for i in range( 0, DEFAULTPLAYER ):
            if i != k:
                pass
        return

    def del_client( self, k ):
        self.clientlock.acquire()
        if self.client[k]:
            self.tlocks[k].acquire()
            self.client[k][0].close()
            self.client[k] = None
            self.remain[k] = None
            self.clientcount -= 1
            self.tlocks[k].release()
            if DEBUG:
                print( 'connection close, Player no ', obj )
        self.clientlock.release()

    def run( self ):
        self.wait4connection()
        self.onmove = random.choice( range( 0, DEFAULTPLAYER ) )
        self.status = CMD_MOVE

        for k in range( DEFAULTPLAYER ):
            thread.start_new( self.run_client, ( k ) )

        #wait for all players to exit...
        while True:
            self.clientlock.acquire()
            if self.clientcount == 0:
                break
            self.clientlock.release()
            time.sleep( 1 )
        self.socket.close()

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

    def wait4connection( self ):
        while True:
            self.add_client()
            self.clientlock.acquire()
            if self.clientcount == DEFAULTPLAYER:
                break
            self.clientlock.release()
            time.sleep( 1 )
"""

if __name__ == '__main__':
    s = SiGuoServer()
    s.run()
