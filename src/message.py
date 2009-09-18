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

#Existed socket
class MsgMixin():
    def __init__( self, socket ):
        self.socket = socket
        #buffer for recv / send in lines
        self.recvstr = ''
        self.sendstr = ''

    def recvline( self ):
        l = self.recvstr.find( '\n' )
        if l == -1:
            while l == -1:
                tmp = self.socket.recv( 512 ).decode( 'utf-8' ) #python 3
                if tmp == '':
                    if self.recvstr != '':
                        ret = self.recvstr
                        self.recvstr = ''
                        return ret
                    else:
                        raise socket.error( 'Connection closed' )
                else:
                    self.recvstr = self.recvstr + tmp
                    l = self.recvstr.find( '\n' )
            ret = self.recvstr[0:l]
            self.recvstr = self.recvstr[( l + 1 ):]
            if define.log_lv & define.LOG_MSG:
                print( 'recv :', ret )
            return ret
        else:
            ret = self.recvstr[0:l]
            self.recvstr = self.recvstr[( l + 1 ):]
            if define.log_lv & define.LOG_MSG:
                print( 'received:', ret )
            return ret

    def sendline( self, target ):
        if self.sendstr:
            target = self.sendstr + target
            self.sendstr = ''
        if not target:
            return
        sent = 0
        count = 0
        for line in target.splitlines():
            lcount = 0
            line = line + '\n'
            while lcount != len( line ):
                m = self.socket.send( line.encode( 'utf-8' ) )
                if m == 0:
                    count += 1
                    if count == MAXERROR:
                        raise socket.error( 'Network is busy' )
                lcount += m
            sent += lcount
            if define.log_lv & define.LOG_MSG:
                print( 'sent :' , line[:-1] )
        return sent

    """
        split a target into three parts
    """
    def split( self , target ):
        if target == None:
            return ( CMD_NONE, None )
        if target == '':
            return ( CMD_COMMENT, '' )
        try:
            cmd, target = target.split( ':', 1 )
            cmd = cmd.strip()
        except Exception as e:
            return ( CMD_COMMENT, target )

        arg = None
        if not ( cmd in msg_cmd ):
            return ( CMD_ERROR, 'unknown keyword' )
        elif cmd in [CMD_COMMENT, CMD_ASK, CMD_ERROR]:
            return ( cmd, target )

        try:
            typ, obj = target.split( ':', 1 )
            typ = typ.strip()
            obj = obj.strip()
        except:
            #treat it as a comment
            return ( CMD_COMMENT, target )

        if cmd == CMD_TELL:
            try:
                objname, obj = obj.split( ':', 1 )
                objname = objname.strip()
                obj = obj.strip()
            except Exception:
                objname = ''

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
                if cmd == CMD_TELL:
                    return ( cmd, ( objname, arg ) )
                else:
                    return ( cmd, arg )
            return ( CMD_COMMENT, target )
        except Exception as e:
            if define.log_lv & define.LOG_MSG:
                print( e )
            return ( CMD_ERROR, target )

    def recv_split( self ):
        target = self.recvline()
        return self.split( target )

    def join( self, cmd, typ, arg ):
        if cmd == CMD_NONE:
            return
        if cmd in [CMD_COMMENT, CMD_ASK, CMD_ERROR]:
            return cmd + ':' + arg
        target = cmd + ':' + typ + ':'
        if cmd == CMD_TELL:
            try:
                target, arg = target + arg[0] + ':', arg[1]
            except Exception:
                target = target + ':'
        if typ == 'str':
            return target + arg
        if typ == 'int':
            return target + str( arg )
        if typ == 'int,int':
            return target + str( arg[0] ) + ',' + str( arg[1] )
        if typ == 'float':
            return target + str( arg )
        return target + '\n'

    def send_join( self, cmd = CMD_NONE, typ = None, arg = None ):
        target = self.join( cmd, typ, arg )
        return self.sendline( target )

    def send_add( self, cmd = CMD_NONE, typ = None, arg = None ):
        self.sendstr = self.sendstr + self.join( cmd, typ, arg )

class MsgSocket( MsgMixin, socket.socket ):
    def __init__( self ):
        socket.socket.__init__( self, socket.AF_INET, socket.SOCK_STREAM )
        MsgMixin.__init__( self, self )

if __name__ == '__main__':
    m = MsgSocket()
    print( m )
