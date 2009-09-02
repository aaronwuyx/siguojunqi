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

from socket import *
from defines import *
import rule, message
import string, random, thread, time

CLIENT_WAIT = 'wait' #Wait for client
CLIENT_MOVE = 'move' #tell a client to move
CLIENT_EXIT = 'exit' #disconnect client

class Server:
    def __init__( self , URL = 'localhost', Port = 30000 ):
        self.status = CLIENT_WAIT #status
        self.extra = None #indicate who move/exit/wait
        #create socket
        self.socket = socket( AF_INET, SOCK_STREAM )
        self.socket.bind( ( URL, Port ) )
        self.socket.listen( 5 )
        #client info
        self.clientcount = 0
        self.client = []
        self.remain = []
        for i in range( DEFAULTPLAYER ):
            self.client.append( None )
            self.remain.append( None )
        #locks
        self.tids = []
        self.clientlock = thread.allocate_lock()
        self.mainlock = thread.allocate_lock()

    def add_client( self ):
        conn, addr = self.socket.accept()
        if DEBUG:
            print 'connection from address ', addr
        player, remain = message.readline( conn, '' )
        k = string.atoi( player.strip() )
        if ( k <= 0 ) | ( k > DEFAULTPLAYER ):
            message.writeline( conn, message.combineline( 'error', 'string', 'invalid player number' ) )
            conn.close()
            return False
        self.clientlock.acquire()
        if self.client[k - 1]:
            message.writeline( conn, message.combineline( 'error', 'string', 'duplicate player number' ) )
            self.clientlock.release()
            conn.close()
            return False
        self.client[k - 1] = ( conn, addr )
        self.remain[k - 1] = remain
        self.clientcount += 1
        self.clientlock.release()
        message.writeline( conn, str( k ) )
        if DEBUG:
            print ' player no ', k
        return k

    def run_client( self, k ):
        while self.status == CLIENT_WAIT:
            pass
        while True:
            data, self.remain[k] = message.readline( self.client[k][0], self.remain[k] )
            if data == '':
                self.client[k] = None
                self.remain[k] = None
                self.clientcount -= 1
                raise Exception('Disconnected from client unknown reason...')
            cmd,arg,obj = message.splitline(data)
            if DEBUG:
                print cmd,arg,obj
            if cmd == 'disconnect':
                message.writeline(str(obj))
                self.client[k][0].close()
                self.client[k]=None
                self.remain[k]=None
                self.clientcount -= 1
                break
            elif cmd == 'move':
                pass

    def run( self ):
        self.wait4connection()
        startup = random.choice( range( 0, DEFAULTPLAYER + 1 ) )
        self.status = CLIENT_EXIT
        for i in range( DEFAULTPLAYER ):
            thread.start_new( self.run_client, () )
#       wait for all thread to stop... then
        self.socket.close()

    def wait4connection( self ):
        while True:
            self.add_client()
            self.clientlock.acquire()
            if self.clientcount == DEFAULTPLAYER:
                break
            self.clientlock.release()
            time.sleep( 1 )

if __name__ == '__main__':
    s = Server()
    s.run()
