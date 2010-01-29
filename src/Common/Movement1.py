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

from Rule import isValidPos

class Movement1():
    def __init__( self, step, fpos, tpos, result ):
        if not isValidPos( fpos ):
            raise ValueError( "Invalid position id %d" % ( fpos ) )
        if not isValidPos( tpos ):
            raise ValueError( "Invalid position id %d" % ( tpos ) )
        if step < 0:
            raise ValueError( "Invalid step number %d" % ( step ) )
        if abs( result ) > 1:
            raise ValueError( "Invalid result %d" % ( result ) )
        self.__count = step
        self.__from = fpos
        self.__to = tpos
        self.__result = result

    def getStep( self ):
        return self.__count

    def getFpos( self ):
        return self.__from

    def getTpos( self ):
        return self.__to

    def getResult( self ):
        return self.__result

    def toString( self ):
        return "%d,%d,%d,%d" % ( self.__count, self.__from, self.__to, self.__result )

def fromString( source ):
    tmp = []
    for item in source.split():
        tmp.append( int( item.trim() ) )
    return Movement1( tmp[0], tmp[1], tmp[2], tmp[3] )
