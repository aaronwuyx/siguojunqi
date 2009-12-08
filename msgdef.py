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
ARGSEP = ',' #list output
MAXERROR = 10 # maximum times of retries before raise exceptions

msg_cmd_list = [CMD_NONE,CMD_ERROR,CMD_ASK,CMD_REPLY,CMD_OTHER,CMD_EXIT,CMD_INFORM,CMD_EXIT]
CMD_NONE = 'None'
CMD_OTHER = 'Comment'
CMD_ERROR = 'Error' #Cause other side of the link to raise an Exception
CMD_ASK = 'Ask' #One side ask any other side some information
CMD_REPLY = 'Reply' #Other side answer for the last Ask
CMD_INFORM = 'Inform' #Server side tells all the clients something
CMD_EXIT = 'Exit' #Client side tells the server to close connection

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
    def __init__(num,fpos,tpos):
        self.num = num
        self.fpos = fpos
        self.tpos = tpos

class Move2():
    def __init__(num,fpos,tpos,result):
        self.num = num
        self.fpos = fpos
        self.tpos = tpos
        self.result = result

"""
what time to use CMD_INFORM keywords

new connection - srv:send data
remove connection - cli:remove data
game finished - srv:send data cli:store data
win - cli:store data
lose - cli:store data
new move - srv:send data cli:sync data
"""
