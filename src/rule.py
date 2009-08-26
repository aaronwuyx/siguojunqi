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
    Initdata = {'value':None, 'player':None, 'status':MAP_NONE}
    def __init__( self, size ):
        self.data = []
        self.size = size
        for i in range( 0, self.size ):
            self.data.append( Map.Initdata )

#use place before game start
    def Place( self, pos, value, player, status = MAP_SHOW ):
        if self.CanPlace( pos, value, player ) == True:
            self.data[pos] = {'value':value, 'player':player, 'status':status}
            return True
        return False

    def CanPlace( self, pos, value, player ):
        rule = GetChessRule( value )
        if ( pos >= player * 30 ) | ( pos < ( player - 1 ) * 30 ):
            return False
        if self.data[pos] != Map.Initdata:
            return False
        pos = pos % 30
        if Pos4[pos].safe:
            return False
        if rule == 0:
            return True
        elif rule == 1:
            return ( pos < 10 )
        elif rule == 2:
            return ( pos < 25 )
        elif rule == 3:
            return ( ( pos == 1 ) | ( pos == 3 ) )
        return False

    def GetValue( self, pos ):
        return self.data[pos]['value']

    def GetPlayer( self, pos ):
        return self.data[pos]['player']

    def GetStatus( self, pos ):
        return self.data[pos]['status']

    def Remove( self, pos ):
        self.data[pos] = Map.Initdata

    def Move( self, fpos, tpos ):
        if self.CanMove( fpos, tpos ):
            result = Result( fpos, tpos )
            if result == 0:
                self.Remove( tpos )
            elif result > 0:
                self.data[tpos] = self.data[fpos]
            self.Remove( fpos )

    def CanMove( self, fpos, tpos ):
        #no chess to move
        if self.data[fpos] == Map.Initdata:
            return False
        #chess cannot move
        if Pos4[fpos].move == False:
            return False
        #position cannot move
        if GetChessMove == 0:
            return False
        #chess in tpos
        if self.data[tpos]['value'] != Map.Initdata:
            if self.data[tpos]['player'] in Team4[self.data[fpos]['player']]:
                return False
        #direct move, 1 step
        if ( OnRailway( fpos ) == ( -1, -1 ) ) | ( OnRailway( tpos ) == ( -1, -1 ) ):
            return ( tpos in Pos4[fpos].link )
        #GoBi's fly
        if GetChessMove == 2:
            return ( tpos in self.GetFlyArea( fpos ) )
        #Railway
        rail, fon, ton = self.OnSameRailway( self, fpos, tpos );
        if ( fon >= 0 ) & ( ton >= 0 ):
            for i in range( fon + 1, ton ):
                if self.data[Railways[rail][i]]['value'] != Map.Initdata:
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
        if self.data[pos]['player'] != player:
            return False
        if Pos4[pos].move == 0:
            return False
        if self.data[pos]['status'] == MAP_NONE:
            return False
        if GetChessMove( self.data[pos]['value'] ) == 0:
            return False
        return True

    def Result( self, fpos, tpos ):
        fval = self.data[fpos]['value']
        tval = self.data[tpos]['value']
        if ( fval == 42 ) | ( tval == 42 ):
            return 0
        if ( fval == 32 ) & ( tval == 41 ):
            return 1
        return ( fval - tval )

class Player():
    def __init__( self ):
        self.name = ''
        self.chess = []
    def Lost( self ):
        return False

if __name__ == '__main__':
    print Map.Initdata
