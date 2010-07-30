#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Positions class.
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

from Position import Position
from Chess import Chess

class Positions(object):
    """
    This class describes a group of Positions.
    It is inherited by ChessBoard / Layout
    
    size - number of positions
    item - a list of positions
        
    Positions(size) : construct positions
    __str__() : output for debugging
    getSize() : number of positions
    getItem() : get an item
    count(pos) - count non-empty positions
        Set(pos,chess) - set chess in position pos
        Get(pos) - get chess in position pos 
        Remove(pos) - remove chess in position pos, return the removed chess
        RemoveAll(pos) - remove all chesses

        Copy(other,start,num) - copy a number of "num" Positions from "other" into Position id "start"
        
    """
    def __init__( self, size ):
        if size < 0:
            self.size = 0
        else:
            self.size = size
        self.type = "POSITIONS"
        
        #initialize with empty position
        self.item = [Position(i) for i in range(self.size)]

    def __str__( self ):
        """
            Positions -> readable Str.
        """
        dlist = [str(self.item[i]) for i in range(self.size)]
        return '\n'.join(dlist)

    def getSize( self ):
        """
            get Position size.
        """
        return self.size

    def getItem( self ):
        """
            get all items.
        """
        return self.item

    def count( self ):
        """
            return number of non-empty Positions.
        """
        count = 0
        for item in self.item:
            if item.isChess():
                count += 1
        return count

    def remove( self, pos ):
        """
            remove the chess in position pos, and return the orignal value.
        """
        tmp = self.item[pos].getChess()
        self.item[pos].setChess( None )
        return tmp

    def removeAll( self ):
        """
            remove all chess.
        """
        for pos in range( self.size ):
            self.item[pos].setChess(None)

    def setChess( self, pos, chess ):
        """
            quick access to pos.setChess().
        """
        self.item[pos].setChess( chess )

    def getChess( self, pos ):
        """
            quick access to pos.getChess().
        """
        return self.item[pos].getChess()

    def getPos( self, pos ):
        """
            get the specified Position.
        """
        return self.item[pos]

    def copy( self, other, start1, start2 = 0, num = -1 ):
        """
            copy chess from another Positions.
        """
        if not other:
            return

        if ( start1 < 0 or start1 >= self.size ):
            start1 = 0

        if ( start2 < 0 or start2 >= other.size ):
            start2 = 0

        if ( num < 0 ) or ( num > other.size - start2 ) or ( num > self.size - start1 ):
            if other.size - start2 > self.size - start1 :
                num = self.size - start1
            else:
                num = other.size - start2;

        for i in range( num ):
            self.item[start1 + i].setChess( other.item[start2 + i].getChess() )

    def copyFrom(self, other, start1):
        if other.size > self.size:
            return
        self.copy(other,start1, 0, -1)
        
if __name__ == '__main__':
        p2 = Positions( 10 );
        p3 = Positions( 5 );
        c = Chess( 1, 0 )
        p2.setChess( 0, c )
        p2.setChess( 1, Chess( 2, 1 ) );
        p3.setChess( 3, Chess( 3, 2 ) );

        print( p2 )
        print( p3 )
        p2.copyFrom( p3, 3 );
        print( p2 )

        p2.copy( p3, 1, 3, 1 );
        print( p2 )
