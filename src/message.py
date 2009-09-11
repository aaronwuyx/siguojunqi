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

import socket
import define
from definemsg import *

"""
CMD_WAIT = 'wait' #Wait for client/server
CMD_MOVE = 'move' #tell server to move...
CMD_ONMOVE = 'onmove' #tell a client to move...
CMD_ADD = 'connect'
CMD_EXIT = 'disconnect'
CMD_PLACE = 'place'
"""

class MsgSocket( socket.socket ):
    def __init__( self, other = None ):
        if other:
            #server: access socket
            self = other
        else:
            #client: create MsgSocket()
            socket.socket.__init__( self, socket.AF_INET, socket.SOCK_STREAM )

        self.remainstr = ''

    def recvline( self ):
        l = self.remainstr.find( '\n' )
        if l == -1:
            while l == -1:
                tmp = self.recv( self, 1024 ).decode( 'utf-8' ) #python 3
                if tmp == '':
                    ret = self.remainstr
                    self.remainstr = ''
                    return ret
                else:
                    self.remainstr = self.remainstr + tmp
                    l = self.remianstr.find( '\n' )
            ret = self.remainstr[0:l]
            self.remainstr = self.remainstr[( l + 1 ):]
            if define.DEBUG:
                print( 'received:', ret )
            return ret
        else:
            ret = self.remainstr[0:l]
            self.remainstr = self.remainstr[( l + 1 ):]
            if define.DEBUG:
                print( 'received:', ret )
            return ret

    def sendline( self, target ):
        if target == None:
            return
        if target[-1] != '\n':
            target = target + '\n'
        sent = 0
        while sent != len( target ):
            m = self.send( target.encode( 'utf-8' ) )
            sent += m
        if define.DEBUG:
            print( 'sent:' + target[:-1] )
        return sent

    """
        split a target into three parts
        cmd  - what this line is sent for
        type - type of obj, a str
        arg  - arguments
        ----------------------------------
        type    type of arg
        str        str
        int        int
        int,int    int,int
        lineup     lineup.__str__
    """
    def split( self , target ):
        if target == None:
            return ( CMD_NONE, None )
        if target == '':
            return ( CMD_COMMENT, '' )
        if target[0] == '#':
            return ( CMD_COMMENT, target[1:] )
        if target[0] == '?':
            return ( CMD_ASK, target[1:] )
        if target[0] == '!':
            return ( CMD_ERROR, target[1:] )
        if target[0] == '|':
            return ( CMD_TELL, target[1:] )
        try:
            cmd, typ, obj = target.split( ':', 2 )
            cmd = cmd.strip()
            typ = typ.strip()
            #obj = obj.strip()
        except:
            #treat it as a comment
            return ( CMD_COMMENT, target )
        if typ == 'str':
            return ( cmd, obj )
        elif typ == 'int':
            try:
                arg = int( obj )
                return ( cmd, arg )
            except Exception as e:
                if define.DEBUG:
                    print( str( e ) )
                return ( CMD_ERROR, target )
        elif typ == 'int,int':
            try:
                x, y = obj.split( ',', 1 )
                v1 = int( x.strip() )
                v2 = int( y.strip() )
                arg = ( v1, v2 )
                return ( cmd, arg )
            except Exception as e:
                if define.DEBUG:
                    print( str( e ) )
                return ( CMD_ERROR, target )
        return ( CMD_COMMENT, target )

    def recv_split( self ):
        target = self.recvline()
        return self.split( target )

    def join( self, cmd, typ, arg ):
        if cmd == CMD_NONE:
            return
        if cmd == CMD_COMMENT:
            return '#' + arg
        if cmd == CMD_ASK:
            return '?' + arg
        target = cmd + ':' + typ + ':'
        if typ == 'str':
            return target + arg
        if typ == 'int':
            return target + str( arg )
        if typ == 'int,int':
            return target + str( arg[0] ) + ',' + str( arg[1] )
        return target + '\n'

    def send_join( self, cmd = CMD_NONE, typ = None, arg = None ):
        target = join( cmd, typ, arg )
        return self.sendline( target )
