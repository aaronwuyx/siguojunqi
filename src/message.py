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

def readline( connection, remainstr ):
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

def writeline( connection, targetstr ):
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
cmd, arg are strings, type of obj depends on arg's value
value of arg    type of obj
'string'            str
'''
def splitline( line ):
    cmd = ''
    arg = ''
    obj = None
    try:
        cmd, arg, line = line.split( ':', 2 )
    except:
        cmd = line
    if arg == 'string':
        obj = line
    return ( cmd, arg, obj )

def combineline( cmd, arg = '', obj = None ):
    line = cmd + ':' + arg + ':' + str( obj ) + '\n'
    return line
