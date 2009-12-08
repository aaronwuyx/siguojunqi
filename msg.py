#!/usr/bin/python
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
import logging

from msgdef import *

DEFAULTPORT = 30000
DEFAULTHOST = 'localhost'

class MsgMixin():
    """
    this class is used with socket, it provides recvline / sendline /
    splitline / combline functions

    class MsgMixin():
        socket - the original socket
        recvstr - received string buffer
        sendstr - sent string buffer
        
    methods:
        recvline - read a line from string buffer
        sendline - write a line to string buffer
        recvlines - read serveral lines from string buffer
        sendlines - write serveral lines to string buffer
    """
    def __init__( self, socket ):
        self.socket = socket
        #buffer for recv / send in lines
        self.recvstr = ''
        self.sendstr = ''

    def recvline( self ):
        """
        return received lines
        """
        l = self.recvstr.find( '\n' )
        if l == -1:
            #no more lines in buffer
            while l == -1:
                tmp = self.socket.recv( 512 ).decode( 'utf-8' ) #python 3
                if tmp == '':
                    if self.recvstr != '':
                        ret = self.recvstr
                        self.recvstr = ''
                        return ret
                    else:
                        logging.exception( 'Connection close' )
                        raise socket.error( 'Connection closed' )
                else:
                    self.recvstr = self.recvstr + tmp
                    l = self.recvstr.find( '\n' )

        ret = self.recvstr[0:l]
        self.recvstr = self.recvstr[( l + 1 ):]
        logging.info( 'recv : ' + str( ret ) )
        return ret

    def recvlines( self ):
        list = []
        list.append( self.recvline() )
        while self.recvstr.find( '\n' ) != -1 :
            ret = self.recvline()
            list.append( ret )
        return list

    def sendline( self, line ):
        if self.sendstr:
            target = self.sendstr + line
        if not target:
            return 0
        if target[-1] != '\n':
            target = target + '\n'

        count = 0
        sent = 0

        while sent != len( target ):
            m = self.socket.send( target.encode( 'utf-8' ) )
            if m == 0:
                count += 1
                if count >= MAXERROR:
                    logging.exception( 'Connection closed or network is busy' )
                    raise socket.error( 'Network is busy' )
            sent += m

        logging.info( ' send : ' + line[:-1] )
        self.sendstr = ''
        return sent

    def sendlines( self, text ):
        """
        text - serveral lines of messages to sent
        return value : bytes of text sent
        """
        sent = 0
        for line in text.splitlines():
            sent = sent + self.sendline( line )
        return sent

    def split( self, target ):
        if not target:
            return ( CMD_NONE, None )
        target = target.strip()
        target0 = target
        try:
            cmd, target = target.split( SEP, 1 )
        except Exception as e:
            return ( CMD_ERROR, 'cannot find sep :' + target0 )

        if not ( cmd in msg_cmd ):
            return ( CMD_ERROR, 'unknown keyword:' + cmd )
        elif cmd in [CMD_COMMENT, CMD_ASK, CMD_ERROR]:
            return ( cmd, target )
        try:
            typestr, argstr = target.split( SEP, 1 )
            types = typestr.split( TYPESEP )
            args = argstr.split( ARGSEP )
        except:
            return ( CMD_ERROR, 'cannot find sep :' + target0 )
        if len( types ) != len( args ):
            return ( CMD_ERROR, 'len(arg) != len(type) :' + target0 )

        total = len( types )
        ret = []
        for count in range( total ):
            typ = types[count].strip()
            try:
                if typ == 'str':
                    ret.append( args[count] )
                elif typ == 'int':
                    ret.append( int( args[count].strip() ) )
                elif typ == 'float':
                    ret.append( float( args[count].strip() ) )
                elif typ == 'lineup':
                    tmp = define.Lineup( -1 )
                    tmp.fromStr( args[count] )
                    ret.append( tmp )
            except Exception as e:
                logging.info(str(e))
                return ( CMD_ERROR, target0 )
        return ( cmd, ret )

    def recv_split( self ):
        target = self.recvline()
        return self.split( target )

    def join( self, cmd, types, arg ):
        """
            types, arg's type string
            arg, a list of values
        """
        if cmd in [CMD_COMMENT, CMD_ASK, CMD_ERROR, CMD_NONE]:
            return cmd + SEP + str( arg )
        target = cmd + SEP
        org = ''
        count = 0
        for typ in types:
            if count != 0:
                target += TYPESEP
                org += ARGSEP
            if typ == 'str':
                org += arg[count]
            elif typ == 'int':
                org += str( arg[count] )
            elif typ == 'float':
                org += str( arg[count] )
            elif typ == 'lineup':
                org += arg[count].toStr()
            target = target + typ
            count += 1
        target += SEP + org + '\n'
        return target

    def send_join( self, cmd = CMD_NONE, typ = None, arg = None ):
        target = self.join( cmd, typ, arg )
        return self.sendline( target )

    def send_add( self, cmd = CMD_NONE, typ = None, arg = None ):
        self.sendstr = self.sendstr + self.join( cmd, typ, arg ) + '\n'

class MsgSocket( MsgMixin, socket.socket ):
    def __init__( self ):
        socket.socket.__init__( self, socket.AF_INET, socket.SOCK_STREAM )
        MsgMixin.__init__( self, self )

if __name__ == '__main__':
    m = MsgSocket()
    s = m.join( CMD_TELL, ( 'str', 'int', 'float' ), ( 'abcde', 3, 3.0 ) )
    print( m.split( s ) )
