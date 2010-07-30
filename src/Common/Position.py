#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Position class.
"""

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

POSFILENAME = 'position.txt'
POSDATA = open( POSFILENAME, 'r' ).readlines()

class Position:
    """
    This class describes a position on chessboard.
    It contains a field to set chess in the position.
    refer to Chess.py for more details.
    
    pos - position identifier
    chess - reference to chess on it
    stat - status : selected?
        
    safe - True if chess in the position cannot attend battle
    movable - True if chess in the position can move
    pic - 0 - rectangle 1 - oval 2 - cross 3 - castle down 4 - castle left 5 - castle up 6 - castle right
    x, y - cursor in a map
    rail - a list of rails pos is on
    llink - a list of nearby pos, not on railway
    rlink - a list of nearby pos on railway
    dir - chess direction 0 - vertical 1 - horizon 2 - either
    
    load(pos) - load position data, here pos is the number of pos in the POSDATA, usually equals to self.pos, but may be not 
    __str__() - debug infomation
    getxxx(...) - get attribution xxx
    setxxx(...) - set attribution xxx
    isxxx(...) - return True if attribution is not None
    """

    def __init__( self, pos ):
        from Rule import isValidPos
        if not isValidPos( pos ):
            raise ValueError( "Invalid position %d" % ( pos ) )
        self.pos = pos
        self.chess = None
        self.stat = False
        self.load()

    def __str__( self ):
        return "Position: pos = %d, x = %d, y = %d, pic = %d, movable = %s, safe = %s, "\
        "directory = %d, rail = %s, llink = %s, rlink = %s, chess = %s, stat = %s"\
               %(self.pos, self.x, self.y, self.pic, self.movable, self.safe,
                 self.direction, self.rail, self.llink, self.rlink, self.chess, self.stat)

    def getPos( self ):
        return self.pos

    def getChess( self ):
        return self.chess

    def setChess( self, chess = None ):
        self.chess = chess

    def isChess( self ):
        return ( self.chess != None )

    def getStat( self ):
        return self.stat

    def setStat( self, stat ):
        self.stat = stat

    def getCursor( self ):
        return ( self.x, self.y )

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def getPicNo( self ):
        return self.pic

    def isMovable( self ):
        return self.movable

    def isSafe( self ):
        return self.safe

    def getDirection( self ):
        return self.direction

    def getRailway( self ):
        return self.rail

    def isRailway( self ):
        return len( self.rail ) > 0

    def getLinkOnLine( self ):
        return list(self.llink)

    def getLinkOnRailway( self ):
        return list(self.rlink)

    def getLink( self ):
        return self.llink + self.rlink

    def getStat(self):
        return self.stat
    
    def load( self ):
        """
            This method reads position data from file, and fill in the
            position pos. An corrupted input file may lead to TypeError
            or ValueError exception
        """
        global POSDATA

        #one position per line, line[pos] => POSDATA[pos]
        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        content =  POSDATA[self.pos].split(':')

        if len(content) < 11:
            raise ValueError( 'Invalid syntax %s' %(content) )

        if (int(content[0]) != self.pos):
            raise ValueError( 'Invalid position data line : %d' % ( self.pos ) )

        self.x, self.y, self.pic, self.movable, self.safe, self.direction = \
                int(content[1]),int(content[2]),int(content[3]),\
                (int(content[4])!=0),(int(content[5])!=0), int(content[6])

        if content[7]:
            self.rail = [int(item) for item in content[7].split(',')]
        else:
            self.rail = []
        if content[8]:
            self.llink = [int(item) for item in content[8].split(',')]
        else:
            self.llink = []
        if content[9]:
            self.rlink = [int(item) for item in content[9].split(',')]
        else:
            self.rlink = []

if __name__ == '__main__':
    from Rule import MAXPOSITION
    for i in range( MAXPOSITION ):
        pos1 = Position( i )
        print( pos1 )
        print( pos1.getLink() )
