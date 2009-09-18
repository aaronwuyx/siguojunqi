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

MAXERROR = 10

#Constants used in Message/Client/Server
CMD_COMMENT = '#' #COMMENTS ONLY, not treated
CMD_ERROR = '!' #error raised in server/client
CMD_NONE = 'none' #nothing
CMD_ASK = '?' #ask for a value, arg indicates its name
CMD_TELL = 'tell' #transfer a return value, typ is its type
CMD_WAIT = 'wait' #tell a client to wait
CMD_EXIT = 'exit' #disconnect
CMD_MOVE = 'move'
msg_cmd = [CMD_COMMENT, CMD_ERROR, CMD_NONE, CMD_ASK, CMD_TELL, CMD_WAIT, CMD_EXIT, CMD_MOVE]

msgdocstr = """
each line transferred can be split into 3 parts
cmd  - what this line is sent for
type - type of obj, a str
arg  - arguments

valid cmd is listed in msg_cmd above.
----------------------------------
value of type      type of arg
        str        str
        int        int
        float      double
----------------------------------
For CMD_TELL's, things are a little different, arg is a tuple
        typ     arg[0]   arg[1]
        int     'id'     id value
        str     'name'   name
        int,int 'move'   fpos,tpos
        str     'lineup' lineup.toStr*

*this will be implemented in next version        
"""

FIL_ID = 'id'
FIL_NAME = 'name'
FIL_LINEUP = 'lineup'
FIL_MOVE = 'move'
