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
import rule
import os, sys, thread, string,random

debug = True

#Server Client
class Server:
    def __init__( self , URL = 'localhost', Port = 30000 ):
        #create socket
        self.socket = socket( AF_INET, SOCK_STREAM )
        self.socket.bind( ( URL, Port ) )
        self.socket.listen( 5 )
        self.socket.setblocking( 0 )

        self.clientcount = 0
        self.client = []
        self.remain = []
        for i in range(DEFAULTPLAYER):
            self.client.append(None)
            self.remain.append(None)
        self.start = random.choice([1,2,3,4])

    def add_client( self ):
        conn, addr = self.socket.accept()
        player, remain = self.readline(conn,'')
        k = string.atoi(player.strip())
        if (k <= 0) | (k > DEFAULTPLAYER):
            conn.close()
        if client[k]:
            self.writeline(conn,'error: duplicate player number')
            conn.close()
        self.client[k] = (conn,addr)
        self.remain[k] = remain
        self.clientcount += 1
        print 'connection from address ', addr,' player no ',k

    def readline( self, connection, remainstr):
        if remainstr.find( '\n' ) == -1:
            len = -1
            try:
                while len == -1:
                    tmp = connection.recv( 1024 )
                    remainstr = remainstr + tmp
                    len = remainstr.find( '\n' )
                ret = remainstr[0:len]
                remainstr = remainstr[( len + 1 ):]
                return ret, remainstr
            except error:
                pass
        else:
            len = remainstr.find( '\n' )
            ret = remainstr[0:len]
            remainstr = remainstr[( len + 1 ):]
            return ret, remainstr

    def writeline( self, connection, targetstr):
        return
    
    def run( self ):
        self.add_client()
        while True:
            for addr in self.client.keys():
                data = self.readline( addr )
                print data
            if data == '':
                break
        self.socket.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        debug = False
    s = Server()
    s.run()
