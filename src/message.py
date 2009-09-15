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
CMD_EXIT = 'disconnect'
CMD_PLACE = 'place'
"""

#Existed socket
class MsgMixin():
    def __init__( self, socket ):
        self.socket = socket
        self.remainstr = ''

    def recvline( self ):
        l = self.remainstr.find( '\n' )
        if l == -1:
            while l == -1:
                tmp = self.socket.recv( 1024 ).decode( 'utf-8' ) #python 3
                if tmp == '':
                    ret = self.remainstr
                    self.remainstr = ''
                    return ret
                else:
                    self.remainstr = self.remainstr + tmp
                    l = self.remainstr.find( '\n' )
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
        count = 0
        while sent != len( target ):
            m = self.socket.send( target.encode( 'utf-8' ) )
            if m == 0:
                count += 1
                if count == 10:
                    raise Exception( 'Network is busy' )
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
        type       type of arg
        str        str
        int        int
        float      double
        int,int    int,int
        lineup     lineup.__str__
    """
    def split( self , target ):
        if target == None:
            return ( CMD_NONE, None )
        if target == '':
            return ( CMD_COMMENT, '' )
        for keyword in [CMD_COMMENT, CMD_ASK, CMD_ERROR]:
            if target[:len( keyword )] == keyword:
                return ( keyword, target[len( keyword ):] )
        arg = None
        try:
            cmd, typ, obj = target.split( ':', 2 )
            cmd = cmd.strip()
            typ = typ.strip()
            obj = obj.strip()
        except:
            #treat it as a comment
            return ( CMD_COMMENT, target )
        if not ( cmd in msg_cmd ):
            return ( CMD_ERROR, 'unknown keyword' )
        try:
            if typ == 'str':
                arg = obj
            elif typ == 'int':
                arg = int( obj )
            elif typ == 'float':
                arg = double( obj )
            elif typ == 'int,int':
                x, y = obj.split( ',', 1 )
                v1 = int( x.strip() )
                v2 = int( y.strip() )
                arg = ( v1, v2 )
            if arg != None:
                return ( cmd, arg )
            return ( CMD_COMMENT, target )
        except Exception as e:
            if define.DEBUG:
                print( str( e ) )
            return ( CMD_ERROR, target )

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
        target = self.join( cmd, typ, arg )
        return self.sendline( target )

class MsgSocket( MsgMixin, socket.socket ):
    def __init__( self ):
        socket.socket.__init__( self, socket.AF_INET, socket.SOCK_STREAM )
        MsgMixin.__init__( self, self )
        print( self.family, ',', self.remainstr )

if __name__ == '__main__':
    m = MsgSocket()
    print( m )
