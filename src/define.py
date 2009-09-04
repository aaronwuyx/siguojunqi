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

import profile

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
        self.selected = False

    #read position settings from file
    def load( self, pos ):
        global POSDATA
        if POSDATA == None:
            POSDATA = open( POSFILENAME, 'r' ).readlines()
        line = POSDATA[pos]
        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 = line.split( ':', 10 )
        cert = int( a1 )
        if cert != pos:
            raise Exception( 'Invalid position data' )

        self.x = int( a2 )
        self.y = int( a3 )
        self.pic = int( a4 )
        self.movable = ( int( a5 ) != 0 )
        self.safe = ( int( a6 ) != 0 )
        self.direct = int( a7 )

        self.rail = []
        if a8 != '':
            for item in a8.split( ',' ):
                self.rail.append( int( item ) )
        self.link = []
        if a9 != '':
            for item in a9.split( ',' ):
                self.link.append( int( item ) )
        self.rlink = []
        if a10 != '':
            for item in a10.split( ',' ):
                self.rlink.append( int( item ) )

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

    def IsChess( self ):
        return ( self.chess != None )

#Replace MAP_*
VIS_NONE = 'none'
VIS_SELF = 'self'
#VIS_TEAM = 'team'
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

class Positions:
    def __init__( self, size ):
        if size <= 0:
            size = MAXPOSITION
        self.size = size
        self.item = []
        for i in range( 0, self.size ):
            self.item.append( Position( i ) )

    #return True if a chess is place in the position
    def Place( self, pos, chess ):
        value = chess.GetValue()
        player = chess.GetPlayer()
        #Not player's field
        if ( pos >= ( player + 1 ) * MAXCHESS ) or ( pos < player * MAXCHESS ):
            return False
        #Safe position
        if self.item[pos].IsSafe():
            return False
        #Chess already
        if self.item[pos].IsChess():
            return False
        if value == None:
            self.item[pos].SetChess( chess )
            return True
        rule = chess.GetInitrule()
        p = pos % MAXCHESS
        #Check according to place rule
        if rule == 0:
            self.item[pos].SetChess( chess )
            return True
        elif ( rule == 1 ) & ( p < 10 ):
            self.item[pos].SetChess( chess )
            return True
        elif ( rule == 2 ) & ( p < 25 ):
            self.item[pos].SetChess( chess )
            return True
        elif ( rule == 3 ) & ( ( p == 1 ) | ( p == 3 ) ):
            self.item[pos].SetChess( chess )
            return True
        return False

    def Remove( self, pos ):
        tmp = self.item[pos].GetChess()
        self.item[pos].SetChess( None )
        return tmp

    def CanSelect( self, pos, player ):
        if self.item[pos].isMovable == False:
            return False
        if self.item[pos].GetChess() == None:
            return False
        if self.item[pos].GetChess().GetPlayer() != player:
            return False
        if self.item[pos].selected:
            return False
        return self.item[pos].GetChess().GetInitmove()

    def PutCovered( self, otherplayer, visible ):
        covered = Chess( None, otherplayer, visible )
        for i in range( MAXCHESS ):
            pos = otherplayer * MAXCHESS + i
            if not self.item[pos].IsSafe():
                self.item[pos].SetChess( covered )

    def Move( self, fpos, tpos, result = None ):
        if self.CanMove( fpos, tpos ):
            if self.item[tpos].IsChess():
                if result == None:
                    result = self.Result( fpos, tpos )
                if result == 0:
                    self.Remove( tpos )
                elif result > 0:
                    self.item[tpos].SetChess( self.item[fpos].GetChess() )
            else:
                self.item[tpos].SetChess( self.item[fpos].GetChess() )
            self.Remove( fpos )
            return True
        return False

    #return True if move from "fpos" to "tpos" is available
    def CanMove( self, fpos, tpos ):
        #no chess to move
        if self.item[fpos].IsChess() == False:
            return False
        #chess cannot move, normally it cannot be selected...
        if self.item[fpos].GetChess().GetMoverule() == False:
            return False
        #position cannot move
        if self.item[fpos].IsMovable() == False:
            return False
        #chess in tpos
        c = self.item[tpos].GetChess()
        if c != None:
            if self.item[tpos].IsSafe():
                return False
            if c.GetPlayer() in profile.Profile.Team[self.item[fpos].GetPlayer()]:
                return False
        #1 step
        if ( not self.item[fpos].IsRailway() ) | ( not self.item[tpos].IsRailway() ):
            return ( tpos in Pos4[fpos].link ) | ( tpos in Pos4[fpos].rlink )
        #'fly'
        if self.item[fpos].GetChess().GetMoverule() == 2:
            return ( tpos in self.GetFlyArea( fpos ) )
        #along railway
############ the only problem remains ############# railways
        for i in self.item[fpos].rail:
            if i in self.item[tpos].rail:
                rail = Railways[i]
                fon = rail.index( fpos )
                ton = rail.index( tpos )
                if ton < fon:
                    continue
                for j in range( fon + 1, ton ):
                    if self.item[rail[j]].IsChess():
                        return False
                return True
############ the only problem remains #############
        return False

    '''
    return a positive value - fpos bigger
           a negative value - tpos bigger
           0 - neither
    '''
    def Result( self, fpos, tpos ):
        fval = self.item[fpos].GetChess().GetValue()
        tval = self.item[tpos].GetChess().GetValue()
        if ( fval == 42 ) | ( tval == 42 ):
            return 0
        if ( fval == 32 ) & ( tval == 41 ):
            return 1
        return ( fval - tval )

    def GetFlyArea( self, pos ):
        ret = {pos:1}
        flag = True
        while flag:
            flag = False
            for k in range( self.size ):
                if ret.has_key( k ):
                    if ret[k] != 0:
                        flag = True
                        for l in self.item[k].rlink:
                            if not ret.has_key( l ):
                                if self.item[l].IsChess():
                                    ret[l] = 0
                                else:
                                    ret[l] = 1
                        ret[k] = 0
            if not flag:
                break
        return ret.keys()

####### Deprecated #######
Railways = [[5, 6, 7, 8, 9], [9, 8, 7, 6, 5], [35, 36, 37, 38, 39], [39, 38, 37, 36, 35], [65, 66, 67, 68, 69], [69, 68, 67, 66, 65], [95, 96, 97, 98, 99], [99, 98, 97, 96, 95],
          [25, 26, 27, 28, 29], [29, 28, 27, 26, 25], [55, 56, 57, 58, 59], [59, 58, 57, 56, 55], [85, 86, 87, 88, 89], [89, 88, 87, 86, 85], [115, 116, 117, 118, 119], [119, 118, 117, 116, 115],
          [5, 10, 15, 20, 25, 127, 126, 125, 89, 84, 79, 74, 69], [69, 74, 79, 84, 89, 125, 126, 127, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 121, 122, 123, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 123, 122, 121, 29, 24, 19, 14, 9],
          [99, 104, 109, 114, 119, 127, 120, 121, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 121, 120, 127, 119, 114, 109, 104, 99],
          [95, 100, 105, 110, 115, 125, 124, 123, 59, 54, 49, 44, 39], [39, 44, 49, 54, 59, 123, 124, 125, 115, 110, 105, 100, 95],
          [5, 10, 15, 20, 25, 119, 114, 109, 104, 99], [99, 104, 109, 114, 119, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 29, 24, 19, 14, 9],
          [39, 44, 49, 54, 59, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 59, 54, 49, 44, 39],
          [69, 74, 79, 84, 89, 115, 110, 105, 100, 95], [95, 100, 105, 110, 115, 89, 84, 79, 74, 69],
          [117, 126, 128, 122, 57], [57, 122, 128, 126, 117],
          [27, 120, 128, 124, 87], [87, 124, 128, 120, 27]]
####### Deprecated #######

if __name__ == '__main__':
    Positions( MAXPOSITION )
