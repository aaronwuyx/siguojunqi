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

import sys
import os
import traceback

import logging
from logger import *

#import message # server / client message

from scstat import *

import profile

STABLEVERSION = '0.08'
STABLESVN = '70'
ChangeLog = ''

MAXPLAYER = 4 #Number of players
MAXPOSITION = 129 #Number of positions
MAXCHESS = 30 #Number of pieces

POSFILENAME = 'position.txt'
POSDATA = None

class Position:
    """
    This class describes a position on chessboard, 
    mainly includes 2 parts - a reference of the chess on it - chess
    and the position itself
    class Position():
        pos - position identifier
        chess - referece to chess on it
        stat - status : selected?
        
        safe - True if chess in the position cannot be removed...
        movable - True if chess in the position can move
        pic - 0 - rectangle 1 - oval 2 - cross 3 - castle down 4 - castle left 5 - castle up 6 - castle right
        x, y - cursor in a map
        rail - a list of rails pos is on
        link - a list of nearby pos, not on railway
        raillink - a list of nearby pos on railway
        direct: chess direction 0 - vertical 1 - horizon 2 - either
    
        load(pos) - load position data, here pos is the number of pos in the POSDATA, usually equals to self.pos, but may be not 
        __str__() - debug infomation
    
    methods:
        getxxx(...) - get attribution xxx
        setxxx(...) - set attribution xxx
        isxxx(...) - return True if attribution is not None
    """

    def __init__( self, pos ):
        self.pos = pos
        self.load( pos )
        self.chess = None
        self.stat = False

    def load( self, pos ):
        """
        this method reads position data from file, and fill in the position pos

        an corrupted input file will lead to TypeError / ValueError exception
        """
        global POSDATA
        if not POSDATA:
            POSDATA = open( POSFILENAME, 'r' ).readlines()

        #one position per line, line[pos] => POSDATA[pos]
        line = POSDATA[pos]

        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 = line.split( ':', 10 )
        cert = int( a1 )
        if cert != pos:
            raise ValueError( 'Invalid position data' )

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

        logging.info( self.__str__() )

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
        return ( self.rail != [] )

    def GetChess( self ):
        return self.chess

    def SetChess( self, chess = None ):
        self.chess = chess

    def IsChess( self ):
        return ( self.chess != None )

    def __str__( self ):
        return str( self.__dict__ )

#values set to Chess.visible
VIS_NONE = 'none'
VIS_SELF = 'self'
VIS_TEAM = 'team' #special rules for players in the same team to see each other's chess
VIS_ALL = 'all'

class Chess:
    """
    This class describes attributions of Chess
    
    Class Chess():
        value - chess value identifier
        name - chess name according to its value
        initnum -  chess number when game starts
        initrule - restruction number that decides its position when game starts
        moverule - restruction of movement
        player - player id of player the belongs to
        visible - the chess's visible mode
    """
    Name = {42:'炸弹', 41:'地雷', 40:'司令', 39:'军长', 38:'师长', 37:'旅长', 36:'团长', 35:'营长', 34:'连长', 33:'排长', 32:'工兵', 31:'军旗'}
    Num = {42:2, 41:3, 40:1, 39:1, 38:2, 37:2, 36:2, 35:2, 34:3, 33:3, 32:3, 31:1}
    #rule: 0-all 1-last two lines 2-not first line 3-unmovable place
    Rule = {42:2, 41:1, 40:0, 39:0, 38:0, 37:0, 36:0, 35:0, 34:0, 33:0, 32:0, 31:1}
    #move: 0-none 1-normal 2-'fly' on railway
    Move = {42:1, 41:0, 40:1, 39:1, 38:1, 37:1, 36:1, 35:1, 34:1, 33:1, 32:2, 31:0}

    def __init__( self, value, player, visible ):
        self.value = value
        if value:
            self.name = Chess.Name[value]
            self.initnum = Chess.Num[value]
            self.initrule = Chess.Rule[value]
            self.moverule = Chess.Move[value]
        self.player = player
        self.visible = visible
        logging.info( self.__str__() )

    def __str__( self ):
        return str( self.__dict__ )

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

    def IsVisible( self, other ):
        if self.visible == VIS_NONE:
            return False
        elif self.visible == VIS_ALL:
            return True
        elif self.visible == VIS_SELF:
            return ( other == self.player )
        elif self.visible == VIS_TEAM:
            return ( other in Profile.Team[self.player] )

class Positions:
    """
    This class describes a group of Positions
    It may be a chessboard / lineup
    class Positions():
        size - number of positions
        item - a list of position
    methods:
        __init__(size) 
        Remove(pos) - remove chess in position
        Set(pos,chess) - set chess in position pos
        Get(pos) - get chess in position pos
        Dump(other,start,num) - copy "num" positions from "other" into position "start"
        RemoveAll(pos) - remove all chess in positions
        Count(pos) - count non-empty positions 
    """
    def __init__( self, size ):
        if size < 0:
            size = 0
        self.size = size
        self.item = []
        #initialize with empty position
        for i in range( 0, self.size ):
            self.item.append( Position( i ) )
        logging.info( self.__str__() )

    def __str__( self ):
        dict = {'size':self.size, 'non-empty':self.Count()}
        return str( dict )

    def Count( self ):
        """
        return number of non-empty Position
        """
        count = 0
        for i in range( 0, self.size ):
            if self.item[i].IsChess():
                count = count + 1
        return count

    def Remove( self, pos ):
        tmp = self.item[pos].GetChess()
        self.item[pos].SetChess( None )
        return tmp

    def Set( self, pos, chess ):
        self.item[pos].SetChess( chess )

    def Get( self, pos ):
        return self.item[pos].GetChess()

    def Dump( self, other, start = 0, num = -1 ):
        if num == -1:
            num = other.size
        pos1 = start
        pos2 = 0
        while ( pos1 < self.size ) & ( pos2 < num ):
            self.item[pos1].SetChess( other.item[pos2].GetChess() )
            pos1 += 1
            pos2 += 1

    def RemoveAll( self ):
        for pos in range( self.size ):
            self.Remove( pos )

class CheckerBoard( Positions ):
    """
    This class describes selection / movement rules on checkboard

    class CheckerBoard(Positions):
    methods:
        __init__():
        CanSelect(pos,player) : return True if player can select position pos
        Move(fpos,tpos,result) : set fpos and tpos value according to result  
        CanMove(fpos,tpos) : return True if move from "fpos" to "tpos" is available
        Result(fpos,tpos) : compare two chess in fpos / tpos
        GetFlyArea(pos) : get all fly areas
    """

    def __init__( self ):
        Positions.__init__( self, MAXPOSITION )

    def CanSelect( self, pos, player ):
        #the position is movable
        if self.item[pos].IsMovable() == False:
            return False
        #chess in position pos
        if not self.item[pos].IsChess():
            return False
        #player owns the chess 
        if self.item[pos].GetChess().GetPlayer() != player:
            return False
        #if self.item[pos].selected:
        #    return False
        #chess can move
        return ( self.item[pos].GetChess().GetMoverule() == 0 )

    def Move( self, fpos, tpos, result = None ):
        """
        also invoke CanMove to validate the move:
        if move is invalid, return False
        otherwise, return True, then change chess in position fpos and tpos 
        whatever result, chess in fpos always disappear
        value of tpos depends on result:
        result > 0 : tpos->chess = fpos->chess
        result < 0 : tpos->chess = tpos->chess
        result = 0 : tpos->chess = None
        """
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

    def CanMove( self, fpos, tpos ):
        #no chess to move
        if self.item[fpos].IsChess() == False:
            return False
        #chess cannot move, normally it cannot be selected...
        if self.item[fpos].GetChess().GetMoverule() == 0:
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
            return ( tpos in self.item[fpos].link ) | ( tpos in self.item[fpos].rlink )
        #'fly'
        if self.item[fpos].GetChess().GetMoverule() == 2:
            return ( tpos in self.GetFlyArea( fpos ) )
        #along railway
############ the only problem remained - railway ############# railways
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
############ the only problem remained - railway #############
        return False

    def Result( self, fpos, tpos ):
        """
        return a positive value - fpos bigger
               a negative value - tpos bigger
               0 - neither
               None - Value Unknown
        """
        try:
            fval = self.item[fpos].GetChess().GetValue()
            tval = self.item[tpos].GetChess().GetValue()
        except TypeError, ValueError:
            return None

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

####### To be deprecated #######
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
####### To be deprecated #######

class Lineup( Positions ):
    """
    this class create a Lineup as player "player", and supports load / save operations  
    
    class Lineup(Positions):
        player - player identifier
    methods:
        __init__(player) :
        SetToDefault : set the lineup as default value (avoid / correct critical errors)
        SetToNone : clean up the lineup
        SetToUnknown : use it when claim the lineup is other player's
        Place(pos, chess, nopt) : put chess in position pos
        Load(filename) : load lineup from file
        Save(filename) : save lineup into file
        fromStr(source) : str -> lineup 
        toStr() : lineup -> str
    """

    def __init__( self, player ):
        Positions.__init__( self, MAXCHESS )
        self.player = player

    def SetToDefault( self ):
        default = [41, 31, 41, 33, 36, \
                   33, 41, 36, 32, 33, \
                   37, 34, 37, \
                   40, 35, 35, 39, \
                   42, 34, 42, \
                   38, 32, 34, 32, 38]
        pos = 0
        for value in default:
            self.item[pos].SetChess( Chess( value, self.player, VIS_SELF ) )
            pos += 1
            if pos >= self.size:
                break
            while self.item[pos].IsSafe():
                self.item[pos].SetChess( None )
                pos += 1

    def SetToNone( self ):
        for pos in range( MAXCHESS ):
            self.item[pos].SetChess( None )

    def SetToUnknown( self ):
        for pos in range( MAXCHESS ):
            if self.item[pos].IsSafe():
                self.item[pos].SetChess( None )
                continue
            self.item[pos].SetChess( Chess( None, self.player, VIS_SELF ) )

    #return True if a chess is place in the position
    #when nopt is True, just return whether place is valid 
    def Place( self, pos, chess, nopt = False ):
        value = chess.GetValue()
        player = chess.GetPlayer()
        #Not player's field
        if ( pos < 0 ) | ( pos >= MAXCHESS ):
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
        #Check according to place rule
        if rule == 0:
            if nopt == False:
                self.item[pos].SetChess( chess )
            return True
        elif ( rule == 1 ) & ( pos < 10 ):
            if nopt == False:
                self.item[pos].SetChess( chess )
            return True
        elif ( rule == 2 ) & ( pos < 25 ):
            if nopt == False:
                self.item[pos].SetChess( chess )
            return True
        elif ( rule == 3 ) & ( ( pos == 1 ) | ( pos == 3 ) ):
            if nopt == False:
                self.item[pos].SetChess( chess )
            return True
        return False

    def fromStr( self, source ):
        tmp = Lineup( self.player )
        count = {}
        for key, value in Chess.Num.items():
            count[key] = value
        pos = 0
        for item in source.strip().split():
            if pos > MAXCHESS:
                break
            value = int( item.strip() )
            if tmp.Place( pos, Chess( value , self.player, VIS_SELF ) ) == False:
                raise Exception( 'Cannot place ' + item + 'at ' + str( pos ) )
            count[value] -= 1
            if count[value] < 0:
                raise Exception( 'Number of ' + item + ' is invalid' )
            pos += 1
            if pos >= self.size:
                break
            while self.item[pos].IsSafe():
                self.item[pos].SetChess( None )
                pos += 1
        for key, value in count.items():
            if value != 0:
                raise Exception( 'Number of chess is invalid.' )
        self.Dump( tmp )

    def toStr( self ):
        ret = ''
        for pos in range( MAXCHESS ):
            if not self.item[pos].IsSafe():
                ret = ret + str( self.item[pos].GetChess().GetValue() ) + ' '
        return ret

    def Load( self, filename ):
        try:
            f = open ( filename, 'r' )
        except:
            log_err()
            raise

        try:
            for line in f.readlines():
                if line[:7] == 'lineup=':
                    self.fromStr( line[7:] )
                else:
                    logging.info( line )
        except:
            log_err()
            raise
        try:
            f.close()
        except:
            pass

    def Save( self, filename ):

        try:
            f = open ( filename, 'w' )
        except:
            log_err()
            raise

        f.write( 'You can comment at anywhere except the next line:\n' )
        f.write( 'lineup=' + self.toStr() + '\n' )

        try:
            f.close()
        except:
            pass

if __name__ == '__main__':
    l = Lineup( 0 )
    l.SetToDefault()
    l.Save( 'test' )
    l.Load( 'test' )
    print( l.toStr() )
    os.remove( 'test' )
    p = CheckerBoard()
