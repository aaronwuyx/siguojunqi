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

"""
    this file mainly describes game's rule by defining class "Map"
"""
def CheckPlace1( placement ):
    if len( placement ) != CHESSNUM:
        return False
    for pos in SafeList:
        if ( placement[pos].player == None ) | ( placement[pos].value == None ):
            return False
    tmp = {}
    for item in Initchess:
        tmp[item.value] = tmp[item.initnum]
    for item in placement:
        tmp[item.getValue()] -= 1
    for ( key, value ) in tmp.items():
        if value != 0:
            return False
    return True

def CheckPlace2( placement ):
    tmp = Map( len( Pos4 ) )
    pos = 0
    for item in placement:
        if item.getValue() != None:
            if tmp.Place( pos, item.getValue(), 1 ) == False:
                return False
        pos += 1
    return True

def PlaceOne( placement, m, player ):
    pos = ( player - 1 ) * 30
    for item in placement:
        m.Remove( pos )
        if item.getValue != None:
            m.Place( pos, item.getValue(), player, item.getStatus() )
        pos += 1
    return

def CleanOne( m, player ):
    pos = ( player - 1 ) * 30
    for i in range( 30 ):
        m.Remove( pos )
        pos += 1
    return
