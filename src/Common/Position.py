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

MAXPOSITION = 129 # Number of positions of a chessboard
POSFILENAME = 'position.txt'
POSDATA = None

class Position:
    """
    This class describes a position on chessboard, 
    mainly includes 2 parts - a reference to the chess on it - chess
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
        llink - a list of nearby pos, not on railway
        rlink - a list of nearby pos on railway
        dir - chess direction 0 - vertical 1 - horizon 2 - either
    
        load(pos) - load position data, here pos is the number of pos in the POSDATA, usually equals to self.pos, but may be not 
        __str__() - debug infomation
    
    methods:
        getxxx(...) - get attribution xxx
        setxxx(...) - set attribution xxx
        isxxx(...) - return True if attribution is not None
    """

    def __init__( self, pos ):
        from Rule import isValidPos
        if not isValidPos( pos ):
            raise ValueError( "Invalid position %d" % ( pos ) )
        self.__pos = pos
        self.__chess = None
        self.__stat = False
        self.load()

    def load( self ):
        """
        this method reads position data from file, and fill in the position pos
        an corrupted input file will lead to TypeError / ValueError exception
        """
        global POSDATA
        if not POSDATA:
            POSDATA = open( POSFILENAME, 'r' ).readlines()

        #one position per line, line[pos] => POSDATA[pos]
        line = POSDATA[self.__pos]

        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 = line.split( ':', 10 )
        cert = int( a1 )
        if cert != self.__pos:
            raise ValueError( 'Invalid position data line : %d' % ( self.pos ) )

        self.__x = int( a2 )
        self.__y = int( a3 )
        self.__pic = int( a4 )
        self.__movable = ( int( a5 ) != 0 )
        self.__safe = ( int( a6 ) != 0 )
        self.__dir = int( a7 )

        self.__rail = []
        if a8 != '':
            for item in a8.split( ',' ):
                self.__rail.append( int( item ) )
        self.__llink = []
        if a9 != '':
            for item in a9.split( ',' ):
                self.__llink.append( int( item ) )
        self.__rlink = []
        if a10 != '':
            for item in a10.split( ',' ):
                self.__rlink.append( int( item ) )

        #logging.info( self.__str__() )

    def getPos( self ):
        return self.__pos

    def getChess( self ):
        return self.__chess

    def setChess( self, chess = None ):
        self.__chess = chess

    def isChess( self ):
        return ( self.__chess != None )

    def getStat( self ):
        return self.__stat

    def setStat( self, stat ):
        self.__stat = stat

    def getCursor( self ):
        return ( self.__x, self.__y )

    def getPicNo( self ):
        return self.__pic

    def isMovable( self ):
        return self.__movable

    def isSafe( self ):
        return self.__safe

    def getDirection( self ):
        return self.__dir

    def getRailway( self ):
        return self.__rail

    def isRailway( self ):
        return ( len( self.__rail ) != 0 )

    def getLinkOnLine( self ):
        return self.__llink

    def getLinkOnRailway( self ):
        return self.__rlink

    def getLink( self ):
        return self.__llink + self.__rlink

    def __str__( self ):
        return str( self.__dict__ )

if __name__ == '__main__':
    for i in range( MAXPOSITION ):
        try:
            pos1 = Position( i )
            print( pos1 )
            print( pos1.getLink() )
        except ValueError:
            e = sys.exc_info()
            print( e[0], e[1] )
            traceback.print_tb( e[2] )
