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
import string, random, thread

class Server:
    def __init__( self , URL = 'localhost', Port = 30000 ):
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
        self.clientlock = thread.allocate_lock()
        self.mainlock = thread.allocate_lock()

    def add_client( self ):
        conn, addr = self.socket.accept()
        if DEBUG:
            print 'connection from address ', addr
        player, remain = message.readline( conn, '' )
        k = string.atoi( player.strip() )
        if ( k <= 0 ) | ( k > DEFAULTPLAYER ):
            conn.close()
        self.clientlock.acquire()
        if self.client[k]:
            message.writeline( conn, 'error: duplicate player number' )
            conn.close()
        self.client[k] = ( conn, addr )
        self.remain[k] = remain
        self.clientcount += 1
        self.clientlock.release()
        message.writeline( conn, str( k ) )
        if DEBUG:
            print ' player no ', k

    def run( self ):
        self.add_client()
        while True:
            for k in range( 4 ):
                if self.client[k]:
                    data, self.remain[k] = message.readline( self.client[k][0], self.remain[k] )
                    print data
                    if data == '':
                        break
        startup = random.choice( [1, 2, 3, 4] )
        self.socket.close()

if __name__ == '__main__':
    s = Server()
    s.run()
