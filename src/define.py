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

import locale

DEBUG = True
STABLEVERSION = '0.05'
STABLESVN = '37'

MAXPLAYER = 4 #Number of players
MAXPOSITION = 129 #Number of positions
MAXCHESS = 30 #Number of pieces

POSFILENAME = 'position.txt'
POSDATA = None

#safe - True if chess in the position cannot be removed...
#movable - True if chess in the position can move
#pic - 0 - rectangle 1 - oval 2 - cross 3 - castle down 4 - castle left 5 - castle up 6 - castle right
#x, y - cursor in a map
#rail - a list of rails pos is on
#link - a list of nearby pos, not on railway
#raillink - a list of nearby pos on railway
#direct: 0 - vertical 1 - horizon 2 - either
class Position:

    def __init__( self, pos ):
        self.pos = pos
        self.load( pos )
        self.chess = None

    #read position settings from file
    def load( self, pos ):
        global POSDATA
        if POSDATA == None:
            POSDATA = open( POSFILENAME, 'r' ).readlines()
        line = POSDATA[pos]
        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 = line.split( ':', 10 )
        cert = locale.atoi( a1 )
        if cert != pos:
            raise Exception( 'Invalid position data' )

        self.x = locale.atoi( a2 )
        self.y = locale.atoi( a3 )
        self.pic = locale.atoi( a4 )
        self.movable = ( locale.atoi( a5 ) != 0 )
        self.safe = ( locale.atoi( a6 ) != 0 )
        self.direct = locale.atoi( a7 )

        self.rail = []
        if a8 != '':
            for item in a8.split( ',' ):
                self.rail.append( locale.atoi( item ) )
        self.link = []
        if a9 != '':
            for item in a9.split( ',' ):
                self.link.append( locale.atoi( item ) )
        self.rlink = []
        if a10 != '':
            for item in a10.split( ',' ):
                self.rlink.append( locale.atoi( item ) )

        if DEBUG:
            print( cert, ':', self.x, self.y, self.pic, self.movable, self.safe, \
                  self.direct, self.rail, self.link, self.rlink, a11 )

    def GetCursor( self ):
        return ( self.x, self.y )

    def GetDirection( self ):
        return self.direct

    def IsMovable( self ):
        return self.movable

    def IsSafe( self ):
        return self.safe

    def GetRailway( self ):
        return self.rail

    def IsRailway( self ):
        return ( self.rail != None )

    def getChess( self ):
        return self.chess

    def setChess( self, chess = None ):
        self.chess = chess

#Replace MAP_*
VIS_NONE = 'none'
VIS_SELF = 'self'
VIS_TEAM = 'team'
VIS_ALL = 'all'

class Chess:

    Name = {42:'炸弹', 41:'地雷', 40:'司令', 39:'军长', 38:'师长', 37:'旅长', 36:'团长', 35:'营长', 34:'连长', 33:'排长', 32:'工兵', 31:'军旗'}
    Num = {42:2, 41:3, 40:1, 39:1, 38:2, 37:2, 36:2, 35:2, 34:3, 33:3, 32:3, 31:1}
    #rule: 0-all 1-last two lines 2-not first line 3-unmovable place
    Rule = {42:2, 41:1, 40:0, 39:0, 38:0, 37:0, 36:0, 35:0, 34:0, 33:0, 32:0, 31:1}
    #move: 0-none 1-normal 2-'fly' on railway
    Move = {42:1, 41:0, 40:1, 39:0, 38:0, 37:0, 36:0, 35:0, 34:0, 33:0, 32:2, 31:0}

    def __init__( self, value, player, visible ):
        self.value = value
        if value:
            self.name = Chess.Name[value]
            self.initnum = Chess.Num[value]
            self.initrule = Chess.Rule[value]
            self.moverule = Chess.Move[value]
        self.player = player
        self.visible = visible

    def GetPlayer( self ):
        return self.player

    def GetValue( self ):
        return self.value

    def GetName( self ):
        return self.name

    def GetInitnum( self ):
        return self.initnum

    def GetInitrule( self ):
        return self.initrule

    def GetMoverule( self ):
        return self.moverule

    def IsVisible( self, viewer ):
        if self.visible == VIS_NONE:
            return False
        elif self.visible == VIS_ALL:
            return True
        elif self.visible == VIS_SELF:
            return ( viewer == self.player )
        #unsupported now
        # elif self.visible == VIS_TEAM:
        #    return ( viewer in self.player.)

if __name__ == '__main__':
    for i in range( MAXPOSITION ):
        Position( i )
