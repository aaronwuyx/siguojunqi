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

message_doc = """
Every line transferred can be split into 3 parts:
1. cmd  - command keywords
2. type - a list of arg's types in string, or a string only
3. arg  - a list of arguments

*All valid command keywords are listed in msg_cmd.
**For CMD_TELL, you can transfer as many arguments as you like.
But in siguo, the following str in arg[0] are called FIL_*,
should not alter the types
"""

'''
a few defines
*SEP : seperator between items
MAXERROR : number of retries before raise exception
'''
SEP = ':'
TYPESEP = ','
ARGSEP = '##'
MAXERROR = 10

'''
Constants used in Client/Server through message
'''
CMD_COMMENT = '#' #COMMENTS ONLY, not treated
CMD_ERROR = '!' #error raised in server/client
CMD_NONE = 'none' #nothing
CMD_ASK = '?' #ask for a value, arg indicates its name
CMD_TELL = 'tell' #transfer a return value, typ is its type
CMD_WAIT = 'wait' #tell a client to wait
CMD_EXIT = 'exit' #disconnect
msg_cmd = [CMD_COMMENT, CMD_ERROR, CMD_NONE, CMD_ASK, CMD_TELL, CMD_WAIT, CMD_EXIT]

''' 
Filters used in CMD_TELL
------------------------------
FILTER NAME Other arguments
'id'        int -> id
'name'      str -> name
'idname'    int -> id,str -> name
'move'      int -> fpos,int -> tpos
'move2'     int -> fpos,int -> tpos,int -> result
'lineup'    str -> lineup.toStr*

*In future, will return instance of Lineup instead of a str        
'''

FIL_ID = 'id'
FIL_NAME = 'name'
FIL_IDNAME = 'idname'
FIL_RIDNAME = 'removeidname'
FIL_LINEUP = 'lineup'
FIL_MOVE = 'move'
FIL_MOVE2 = 'move2'
FIL_LOSE = 'lose'
FIL_WIN = 'win'
