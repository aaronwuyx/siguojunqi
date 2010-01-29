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

from Position import Position
class Positions:
    """
    This class describes a group of Positions
    It is inherited by Chessboard / Lineup
    
    class Positions():
        size - number of positions
        item - a list of positions
        
    methods:
        __init__(size) 
        __str__()
        getSize()
        getItem()
        count(pos) - count non-empty positions
        Set(pos,chess) - set chess in position pos
        Get(pos) - get chess in position pos 
        Remove(pos) - remove chess in position pos, return the removed chess
        RemoveAll(pos) - remove all chesses

        Copy(other,start,num) - copy a number of "num" Positions from "other" into Position id "start"
        
    """
    def __init__( self, size ):
        if size <= 0:
            raise ValueError( "Invalid array size" )
        self.__size = size
        self.__item = []
        #initialize with empty position
        for i in range( 0, self.__size ):
            self.item.append( Position( i ) )

        #logging.info( self.__str__() )

    def __str__( self ):
        dict = {'size':self.__size, 'non-empty':self.Count()}
        return str( dict )

    def getSize( self ):
        return self.__size

    def getItem( self ):
        return self.__item

    def count( self ):
        """
        return number of non-empty Position
        """
        count = 0
        for i in range( self.__size ):
            if self.__item[i].isChess():
                count = count + 1
        return count

    def remove( self, pos ):
        tmp = self.__item[pos].getChess()
        self.__item[pos].setChess( None )
        return tmp

    def removeAll( self ):
        for pos in range( self.__size ):
            self.remove( pos )

    def setChess( self, pos, chess ):
        self.__item[pos].setChess( chess )

    def getChess( self, pos ):
        return self.__item[pos].getChess()

    def getPos( self, pos ):
        return self.__item[pos]

    def copy( self, other, start1, start2 = 0, num = -1 ):
        if not other:
            return

        if ( start1 < 0 or start1 >= self.__size ):
            start1 = 0

        if ( start2 < 0 or start2 >= other.__size ):
            start2 = 0

        if ( num < 0 ) or ( num > other.__size - start2 ) or ( num > self.__size - start1 ):
            if other.__size - start2 > self.__size - start1 :
                num = self.__size - start1
            else:
                num = other.__size - start2;

        for i in range( num ):
            self.__item[start1 + i].setChess( other.__item[start2 + i].getChess() )

if __name__ == '__main__':
        p2 = Positions( 10 );
        p3 = Positions( 5 );
        from Chess import Chess
        c = Chess( 1, 0 )
        p2.setChess( 0, c )
        p2.setChess( 1, Chess( 2, 1 ) );
        p3.setChess( 3, Chess( 3, 2 ) );

        print( p2 )
        print( p3 )
        p2.copy( p3, 3 );
        print( p2 )

        p2.copy( p3, 1, 3, 1 );
        print( p2 )
