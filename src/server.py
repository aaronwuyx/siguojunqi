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
import os, sys

class Server:
    def __init__( self , URL = 'localhost', Port = 30000 ):
        self.socket = socket( AF_INET, SOCK_STREAM )
        self.socket.bind( ( URL, Port ) )
        self.socket.listen( 5 )
        self.client = []

    def add_client( self ):
        conn, addr = self.socket.accept()
        self.client.append( {'conn':conn, 'addr':addr} )
        print 'connection = ', conn
        print 'address = ', addr
        self.socket.setblocking( 0 )

    def run( self ):
        self.add_client()

if __name__ == '__main__':
    s = Server()
    s.run()
