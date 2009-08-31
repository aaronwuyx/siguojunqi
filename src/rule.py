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

from defines import *

class Map:
    def __init__( self, size ):
        self.item = []
        self.size = size
        for i in range( 0, self.size ):
            self.item.append( MapItem() )

    #True if chess in pos
    def isPos( self, pos ):
        if self.item[pos].getValue():
            return True
        if self.item[pos].getPlayer():
            return True
        return False

    """
        Place is used before game start, in the place stage
        pos : position id
        value : chess value
        player : chess owner
        status : chess status
    """
    def Place( self, pos, value, player, status = MAP_SHOW ):
        if self.CanPlace( pos, value, player ) == True:
            self.item[pos] = MapItem( value, player, status )
            return True
        else:
            return False

    """
        return True if a chess can be put in the position
    """
    def CanPlace( self, pos, value, player ):
        #Not owner's field
        if ( pos >= player * 30 ) | ( pos < ( player - 1 ) * 30 ):
            return False
        #chess already
        if self.isPos( pos ):
            return False
        #cannot place in safe area
        if Pos4[pos].safe:
            return False
        rule = GetChessRule( value )
        pos = pos % 30
        #Check according to place rule
        if rule == 0:
            return True
        elif rule == 1:
            return ( pos < 10 )
        elif rule == 2:
            return ( pos < 25 )
        elif rule == 3:
            return ( ( pos == 1 ) | ( pos == 3 ) )
        return False

    def Remove( self, pos ):
        if self.isPos( pos ):
            tmp = self.item[pos]
        else:
            tmp = MapItem()
        self.item[pos] = MapItem()
        return tmp

    def Move( self, fpos, tpos ):
        if self.CanMove( fpos, tpos ):
            if self.isPos( tpos ):
                result = Result( fpos, tpos )
                if result == 0:
                    self.Remove( tpos )
                elif result > 0:
                    self.item[tpos] = self.item[fpos]
            else:
                self.item[tpos] = self.item[fpos]
            self.Remove( fpos )
            return True
        return False

    #True if move from "fpos" to "tpos" is available
    def CanMove( self, fpos, tpos ):
        #no chess to move
        if not self.isPos( fpos ):
            return False
        #chess cannot move
        if Pos4[fpos].move == False:
            return False
        #position cannot move
        if self.item[fpos].getMove() == 0:
            return False
        #already chess in tpos
        if self.isPos( tpos ):
            if Pos4[tpos].safe:
                return False
            if self.item[tpos].getPlayer() in Team4[self.item[fpos].getPlayer()]:
                return False
        #direct move, 1 step
        if ( self.OnRailway( fpos ) == ( -1, -1 ) ) | ( self.OnRailway( tpos ) == ( -1, -1 ) ):
            return ( tpos in Pos4[fpos].link )
        #GoBi's fly
        if self.item[fpos].getMove() == 2:
            return ( tpos in self.GetFlyArea( fpos ) )
        #along railway
        rail, fon, ton = self.OnSameRailway( fpos, tpos );
        #Yeah, they are on the same railway
        if ( fon >= 0 ) & ( ton >= 0 ):
            for i in range( fon + 1, ton ):
                if self.isPos( Railways[rail][i] ):
                    return False
            return True
        return False

    def GetFlyArea( self, pos ):
        ret = {pos:1}
        flag = True
        while flag:
            flag = False
            for k in range( self.size ):
                if ret.has_key( k ):
                    if ret[k] != 0:
                        flag = True
                        for railway in Railways:
                            rail = Railways.index( railway )
                            try:
                                f = railway.index( k )
                                l = Railways[rail][f + 1]
                                if not ret.has_key( l ):
                                    if self.isPos( l ):
                                        ret[l] = 0
                                    else:
                                        ret[l] = 1
                            except:
                                pass
                        ret[k] = 0
            if not flag:
                break
        return ret.keys()

    def OnSameRailway( self, pos1, pos2 ):
        for railway in Railways:
            try:
                off1 = railway.index( pos1 );
                off2 = railway.index( pos2 );
                if off1 < off2:
                    return ( Railways.index( railway ), off1, off2 )
            except:
                pass
        return ( -1, -1, -1 )

    def OnRailway( self, pos ):
        for railway in Railways:
            if pos in railway:
                return ( Railways.index( railway ), railway.index( pos ) );
        return ( -1, -1 )

    def CanSelect( self, pos, player ):
        if self.item.getPlayer() != player:
            return False
        if Pos4[pos].move == 0:
            return False
        if self.item[pos].getValue() == None:
            return False
        return ( self.item[pos].getMove() != 0 )

    def Result( self, fpos, tpos ):
        fval = self.item[fpos].getValue()
        tval = self.item[tpos].getValue()
        if ( fval == 42 ) | ( tval == 42 ):
            return 0
        if ( fval == 32 ) & ( tval == 41 ):
            return 1
        return ( fval - tval )

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

class Player():
    def __init__( self ):
        self.name = ''
        self.chess = []
    def Lost( self ):
        return False
    def Lost2( self ):
        return False

if __name__ == '__main__':
    print Map( len( Pos4 ) ).item
