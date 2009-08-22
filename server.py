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

from Defines import *
import rule, message
import os, sys

class Server:
    def __init__( self ):
        self.client = []
    def wait4Connection( self ):
        while True:
            s = Message().receive()
            if s.cmd == 'connect':
                self.client.append()
                #create for new thread...
                if len( self.client ) == MAXPLAYER:
                    break
            elif s.cmd == 'disconnect':
                #kill the thread...
                self.client.remove()
            else:
                continue
    def run( self ):
        self.wait4Connection()
        return

if __name__ == '__main__':
    s = Server()
    s.run()
