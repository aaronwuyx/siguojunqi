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

from defines import *

class Map:
    def __init__( self, size ):
        self.item = []
        self.size = size
        for i in range( 0, self.size ):
            self.item.append( MapItem() )

#use place before game start
    def Place( self, pos, value, player, status = MAP_SHOW ):
        if self.CanPlace( pos, value, player ) == True:
            self.item[pos] = MapItem( value, player, status )
            return True
        else:
            return False

    def CanPlace( self, pos, value, player ):
        if ( pos >= player * 30 ) | ( pos < ( player - 1 ) * 30 ):
            return False
        if self.item[pos].getPlayer():
            return False
        elif self.item[pos].getValue():
            return False
        if Pos4[pos].safe:
            return False
        rule = GetChessRule( value )
        pos = pos % 30
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
        self.item[pos] = MapItem()

    def Move( self, fpos, tpos ):
        if self.CanMove( fpos, tpos ):
            result = Result( fpos, tpos )
            if result == 0:
                self.Remove( tpos )
            elif result > 0:
                self.item[tpos] = self.item[fpos]
            self.Remove( fpos )

    def CanMove( self, fpos, tpos ):
        #no chess to move
        if ( self.item[fpos].getPlayer() != None ) | ( self.item[fpos].getValue() != None ):
            return False
        #chess cannot move
        if Pos4[fpos].move == False:
            return False
        #position cannot move
        if self.item[fpos].getMove() == 0:
            return False
        #chess in tpos
        if self.item[tpos].getPlayer():
            if self.item[tpos].getPlayer() in Team4[self.item[fpos].getPlayer()]:
                return False
        #direct move, 1 step
        if ( OnRailway( fpos ) == ( -1, -1 ) ) | ( OnRailway( tpos ) == ( -1, -1 ) ):
            return ( tpos in Pos4[fpos].link )
        #GoBi's fly
        if self.item[fpos].getMove() == 2:
            return ( tpos in self.GetFlyArea( fpos ) )
        #Railway
        rail, fon, ton = self.OnSameRailway( self, fpos, tpos );
        if ( fon >= 0 ) & ( ton >= 0 ):
            for i in range( fon + 1, ton ):
                if self.item[Railways[rail][i]].getPlayer():
                    return False
        return True

    def GetFlyArea( self, pos ):
        ret = []
#TODO 3 : get the area...        tmp = []
        return ret

    def OnSameRailway( self, pos1, pos2 ):
        for railway in Railways:
            try:
                off1 = railway.index( pos1 );
                off2 = railway.index( pos2 );
                if off1 < off2:
                    return ( railway.index, off1, off2 )
            except:
                pass
        return ( -1, -1, -1 )

    def OnRailway( self, pos ):
        for railway in Railways:
            if pos in railway:
                return railway.index( railway.index, pos1 );
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
    if len( placement ) != 30:
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
