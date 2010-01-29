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

from Positions import Positions
from Chess import Chess
from Chess import MAXINITCHESS
from Rule import canPlaceLayout
MAXCHESS = 30 #Number of positions of a layout

def load( filename, owner ):
    f = open ( filename, 'r' )
    for line in f.readlines():
        if line.startswith( "lineup=" ) or line.startswith( "layout=" ):
            ret = fromString( line[7:], owner )
            f.close()
            return ret
    f.close()
    return None

def fromString( source, owner ):
    ret = Layout( owner )
    count = []
    for inum in Chess.InitNum:
        count.append( inum )
    pos = 0
    p = source.split()
    if ( len( p ) > MAXINITCHESS ) or ( len( p ) <= 0 ):
        raise ValueError( "Invalid layout string " + source )
    for valstr in p:
        val = int( valstr.strip() )
        ch = Chess( val, owner )
        if not canPlaceLayout( ret, pos, ch ):
            raise ValueError( "Invalid layout string " + source )
        else:
            ret.setChess( pos, ch )
        count[val] -= 1
        if count[val] < 0:
            raise ValueError( "Invalid layout string " + source )
        pos += 1
        if pos >= MAXCHESS:
            break
        while ret.getPos( pos ).isSafe():
            ret.setChess( pos, None )
            pos += 1
    for cnt in count:
        if cnt:
            raise ValueError( "Invalid layout string " + source )
    return ret

class Layout( Positions ):
    DefaultLayout = [11, 1, 11, 3, 6, \
                   3, 11, 6, 2, 3, \
                   7, 4, 7, \
                   10, 5, 5, 9, \
                   12, 4, 12, \
                   8, 2, 4, 2, 8]

    def __init__( self, player ):
        Positions.__init__( self, MAXCHESS )
        self.__player = player

    def setToDefault( self ):
        pos = 0
        for value in Layout.DefaultLayout:
            self.setChess( pos, Chess( value, self.player ) )
            pos += 1
            if pos >= self.getSize():
                break
            while self.getPos( pos ).isSafe():
                self.SetChess( pos, None )
                pos += 1

    def setToUnknown( self ):
        for pos in range( self.getSize() ):
            if self.getPos( pos ).isSafe():
                self.setChess( pos, None )
            else:
                self.setChess( pos, Chess( 0, self.__player ) )

    def toString( self ):
        ret = ''
        for pos in range( self.getSize() ):
            if not self.getPos( pos ).isSafe():
                if self.getPos( pos ).isChess():
                    ret = ret + self.getChess().getValue().__str__()
                else:
                    ret = ret + '0'
                ret = ret + ' '
        return ret

    def save( self, filename ):
        if self.count() != MAXINITCHESS:
            raise ValueError( "Invalid layout status" )
        f = open ( filename, 'w' )
        f.write( "Add comment anywhere except line start with 'layout='\n" )
        f.write( 'layout=' + self.toString() + '\n' )
        f.close()

    def __str__( self ):
        return self.toString()

if __name__ == '__main__':
    l = Layout( 0 );
    l.setToDefault()
    p = l.toString()
    l1 = fromString( p, 0 )
    print( l1 )
    try:
        l1.save( "test" )
        l2 = load( "test", 1 )
        print( l2 )
    except IOError as e:
        e.print_exc()
