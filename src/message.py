# -*- coding:utf-8 -*-
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
import string

CMD_WAIT = 'wait' #Wait for client/server
CMD_MOVE = 'move' #tell server to move...
CMD_ONMOVE = 'onmove' #tell a client to move...
CMD_ADD = 'connect'
CMD_EXIT = 'disconnect'
CMD_PLACE = 'place'
CMD_ERROR = 'error'

def Recvline( connection, remainstr ):
    if remainstr.find( '\n' ) == -1:
        len = -1
        try:
            while len == -1:
                tmp = connection.recv( 1024 )
                remainstr = remainstr + tmp
                len = remainstr.find( '\n' )
            ret = remainstr[0:len]
            remainstr = remainstr[( len + 1 ):]
            if DEBUG:
                print 'recv :', ret
            return ret, remainstr
        except error:
            pass
    else:
        len = remainstr.find( '\n' )
        ret = remainstr[0:len]
        remainstr = remainstr[( len + 1 ):]
        if DEBUG:
            print 'recv :', ret
        return ret, remainstr

def Sendline( connection, targetstr ):
    if ( targetstr == None ) | ( targetstr == '' ):
        return
    if targetstr[-1] != '\n':
        targetstr = targetstr + '\n'
    sent = 0
    while sent != len( targetstr ):
        sent += connection.send( targetstr )
    if DEBUG:
        print 'send :', targetstr[:-1]
    return sent

'''
cmd -     indicate what this line is done for...
arg -     the type of obj
obj -     extra arguments
---------------------------------
cmd        action

---------------------------------
arg                type of obj
'string'             str
'int'                int
'int,int'            int,int
'''
def Sepline( line ):
    cmd = ''
    arg = ''
    obj = None
    try:
        cmd, arg, line = line.split( ':', 2 )
    except:
        cmd = line
        return ( cmd, '', None )
    if arg == 'string':
        obj = line
    elif arg == 'int':
        try:
            obj = string.atoi( line.strip() )
        except:
            pass
    elif arg == 'int,int':
        try:
            l1, l2 = line.split( ',', 1 )
            v1 = string.atoi( l1.strip() )
            v2 = string.atoi( l2.strip() )
            obj = ( v1, v2 )
        except:
            pass
    return ( cmd, arg, obj )

def Combline( cmd, arg = '', obj = None ):
    line = cmd + ':' + arg + ':'
    if arg == 'string':
        line = line + obj
    elif arg == 'int':
        line = line + str( obj )
    elif arg == 'int,int':
        line = line + str( obj[0] ) + ',' + str( obj[1] )
    line = line + '\n'
    return line
