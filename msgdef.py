#!/usr/bin/python
# -*- coding:utf-8 -*-

import define
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

"""
    Use MsgSocket or MsgMixin to send lines of text
    This module describes the format of messages transferred.

    Normally, every line of message can be split into three parts, they are:
    cmd  - command keyword
    arg  - a list of arguments for "cmd"
    type - a string to indicate "arg" types

    They are in the order of "cmd, type, arg", they are seperate by SEP,ARGSEP
    cmd, SEP, type, SEP, arg (seperated by ARGSEP)
    msg_cmd_list describes a list of valid command keywords
    type_char lists all available types    
"""

SEP = '|'
ARGSEP = '#' #list output
MAXERROR = 10 # maximum times of retries before raise exceptions

CMD_NONE = 'None'
CMD_OTHER = 'Comment'
CMD_ERROR = 'Error' #Cause other side of the link to raise an Exception
CMD_ASK = 'Ask' #One side ask any other side some information
CMD_REPLY = 'Reply' #Other side answer for the last Ask
CMD_INFORM = 'Inform' #Server side tells all the clients something
CMD_EXIT = 'Exit' #Client side tells the server to close connection
msg_cmd_list = [CMD_NONE, CMD_ERROR, CMD_ASK, CMD_REPLY, CMD_OTHER, CMD_EXIT, CMD_INFORM, CMD_EXIT]

"""
Mapping character in string "type" into other type, only support limited types
i,I - int
s,S - str
f,F - float
0   - Lineup
1   - Move1 (int,int,int)
2   - Move2 (int,int,int,int)
"""

class Move1():
    def __init__( self, num, fpos, tpos ):
        self.num = num
        self.fpos = fpos
        self.tpos = tpos

    def toStr( self ):
        return str( self.num ) + ':' + str( self.fpos ) + ':' + str( self.tpos )

    def fromStr( self ):
        pass

class Move2():
    def __init__( self, num, fpos, tpos, result ):
        self.num = num
        self.fpos = fpos
        self.tpos = tpos
        self.result = result

    def toStr( self ):
        return str( self.num ) + ':' + str( self.fpos ) + ':' + str( self.tpos ) + ':' + str( self.result )

    def fromStr( self ):
        pass

def join( cmd, type, value ):
    """
    This program may raise ValueError / TypeError
    """
    if not ( cmd in msg_cmd_list ):
        raise ValueError( 'UNKNOWN CMD' + cmd )
    ret = cmd
    if not type:
        return ret
    ret = ret + SEP + type + SEP
    for i in range( len( type ) ):
        ch = type[i]
        if i > 0:
            ret = ret + ARGSEP
        if ch == 'i' or ch == 'I':
            ret = ret + str( value[i] )
        elif ch == 's' or ch == 'S':
            ret = ret + value[i]
        elif ch == 'f' or ch == 'F':
            ret = ret + str( value[i] )
        elif ch == '0':
            ret = ret + value[i].toStr()
        elif ch == '1':
            ret = ret + value[i].toStr()
        elif ch == '2':
            ret = ret + value[i].toStr()
        else:
            raise TypeError( 'Unknown type of value' )
    return ret

def split( source ):
    if not source:
        return ( CMD_NONE, '', None )
    source = source.strip()
    try:
        cmd, typ, arg = source.split( SEP, 2 )
    except ValueError:
        if source in msg_cmd_list:
            cmd = source
            typ = ''
            arg = None
        else:
            raise ValueError( 'INVALID SYNTAX' )
    if not ( cmd in msg_cmd_list ) :
        raise ValueError( 'UNKNOWN CMD' )
    if typ:
        ret = []
        arg = arg.split( ARGSEP )
        if len( arg ) != len( typ ):
            raise ValueError( "TYPE AND ARG DOESN'T MATCH" )

        for i in range( len( typ ) ):
            ch = typ[i]
            argk = arg[i].strip()
            if ch == 'i' or ch == 'I':
                num = int( argk )
                ret.append( num )
            elif ch == 's' or ch == 'S':
                ret.append( argk )
            elif ch == 'f' or ch == 'F':
                num = float( argk )
                ret.append( num )
            elif ch == '0':
                l = define.Lineup( 0 )
                l.fromStr( argk )
                ret.append( l )
            elif ch == '1':
                u1, u2, u3 = argk.split( ':' , 2 )
                u1 = int( u1 )
                u2 = int( u2 )
                u3 = int( u3 )
                m = Move1( u1, u2, u3 )
                ret.append( m )
            elif ch == '2':
                u1, u2, u3, u4 = argk.split( ':', 3 )
                u1 = int( u1 )
                u2 = int( u2 )
                u3 = int( u3 )
                u4 = int( u4 )
                m = Move2( u1, u2, u3, u4 )
                ret.append( m )
            else:
                raise TypeError( "UNKNOWN TYPE OF ARGS" )
    return ( cmd, typ, ret )

"""
what time to use CMD_INFORM keywords

new connection - srv:send data
remove connection - cli:remove data
game finished - srv:send data cli:store data
win - cli:store data
lose - cli:store data
new move - srv:send data cli:sync data
"""

"""
CLIENT COMMUNICATION PROGRAM:
S = SEND()
R = RECV()
WHILE R != WAIT | REPLY
    CASE R
        S = SEND()
    R = RECV()

IF R = REPLY:
        
ELIF R = WAIT:
    RETURN
"""

""" 
SERVER COMMUNICATION PROGRAM:
R = RECV()
CASE R
    S = SEND()
RETURN
"""

PLY_ADD = 'add'
PLY_RMV = 'rem'
PLY_MDF = 'mod'

"""
WHEN TRANSFER CMD ON Network
INFORM "IS0" STARTUP INFORM MESSAGE
INFORM "1" / "2" INFORM A STEP
INFORM "SIS" INFORM A PLAYER ADD/REMOVE/MODIFY
ASK "I" ASK A STEP
"""

if __name__ == '__main__':
    l = define.Lineup( 0 )
    l.SetToDefault()
    u = Move1( 3, 4 , 5 )
    v = Move2( 3, 4, 5, 6 )
    s = join( CMD_INFORM, 'si012', ['abcd', 35, l, u, v] )
    print s
    print split( s )
