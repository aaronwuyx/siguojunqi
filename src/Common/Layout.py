#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file describes Layout class, it also supports convertion between
    Layout and Str
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

from Positions import Positions
from Chess import Chess

class Layout( Positions ):
    """
        This class creates a layout. Layout extends Positions.

        Layout(player) : creates an empty layout.
        setToDefault() : set layout to default value. (mine)
        setToUnknown() : set layout to default value. (other)
        toString() : layout -> string convertion.
        fromString(source, owner) : string -> layout convertion.
        save(filename) : save layout into file.
        load(filename, owner) : load layout from file.
        
    """
    defaultLayout = [11, 1, 11, 3, 6, \
                   3, 11, 6, 2, 3, \
                   7, 4, 7, \
                   10, 5, 5, 9, \
                   12, 4, 12, \
                   8, 2, 4, 2, 8]

    def __init__( self, player ):
        from Rule import MAXCHESS
        Positions.__init__( self, MAXCHESS )
        self.player = player
        self.type = "LAYOUT"
        
    def setToDefault( self ):
        pos = 0
        for value in Layout.defaultLayout:
            self.setChess( pos, Chess( value, self.player ) )
            pos += 1
            if pos >= self.getSize():
                break
            while self.getPos( pos ).isSafe():
                self.setChess( pos, None )
                pos += 1

    def setToUnknown( self ):
        for Pos in self.item:
            if Pos.isSafe():
                Pos.setChess( None )
            else:
                Pos.setChess(Chess( 0, self.player ) )

    def toString( self ):
        list = [str(self.getChess(pos).getValue()) for pos in range(self.getSize()) if self.getPos(pos).isSafe() == False]
        return ' '.join(list)

    def fromString(cls, source, owner):
        from Rule import MAXINITCHESS
        from Rule import MAXCHESS
        from Rule import canPlace
        ret = Layout(owner)
        count = list(Chess.InitNum)
        p = source.split()
        if len(p) != MAXINITCHESS:
            raise ValueError("Invalid layout string %s" %(source))
        pos = 0

        for valstr in p:
            val = int(valstr.strip())
            ch = Chess(val, owner)
            if not canPlace( ret, pos, ch ):
                raise ValueError( "Invalid layout string %s" %(source) )
            else:
                ret.setChess( pos, ch )
            count[val] -= 1
            if count[val] < 0:
                raise ValueError( "Invalid layout string %s" %(source) )
            pos += 1
            if pos >= MAXCHESS:
                break
            while ret.getPos( pos ).isSafe():
                ret.setChess( pos, None )
                pos += 1
        return ret

    fromString = classmethod(fromString)
    
    def load(cls, filename, owner ):
        f = open ( filename, 'r' )
        line = f.readline()
        while line != '':
            if line.startswith( "lineup=" ) or line.startswith( "layout=" ):
                ret = Layout.fromString( line[7:], owner )
                f.close()
                return ret
            line = str.strip(f.readline())
        f.close()
        return None

    load = classmethod(load)
    
    def save( self, filename ):
        from Rule import MAXINITCHESS
        if self.count() != MAXINITCHESS:
            raise ValueError( "Invalid layout status" )
        f = open ( filename, 'w' )
        f.write( "You can add any comment except the line start with 'layout='\n" )
        f.write( 'layout=' + self.toString() + '\n' )
        f.close()

    def __str__( self ):
        return self.toString()

if __name__ == '__main__':
    l = Layout( 0 );
    l.setToDefault()
    p = l.toString()
    l1 = Layout.fromString( p, 0 )
    print( l1 )
    try:
        l1.save( "test" )
        l2 = Layout.load( "test", 1 )
        print( l2 )
    except IOError as e:
        e.print_exc()
