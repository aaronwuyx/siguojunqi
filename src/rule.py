from defines import *

class Map:
    def __init__( self, size ):
        self.data = []
        self.size = size
        for i in range( 0, self.size ):
            self.data.append( {'value':None, 'player':None} )

#use place before game start
    def Place( self, pos, value, playno ):
        if self.CanPlace( pos, value, playno ) == True:
            self.data[pos]['value'] = value
            self.data[pos]['player'] = playno
            return True
        return False

    def CanPlace( self, pos, value, playno ):
        rule = self.GetRule( value )
        if ( pos >= playno * 30 ) | ( pos < ( playno - 1 ) * 30 ):
            return False
        if self.data[pos]['value']:
            return False
        if self.data[pos]['player']:
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

    def GetName( self, value ):
        for prop in InitChess:
            if prop.value == value:
                return prop.name

    def GetRule( self, value ):
        for prop in InitChess:
            if prop.value == value:
                return prop.initrule

    def GetMovable( self, value ):
        for prop in InitChess:
            if prop.value == value:
                return prop.move

    def Remove( self, pos ):
        self.data[pos]['value'] = None
        self.data[pos]['player'] = None

    def Move( self, fpos, tpos ):
        if self.CanMove( fpos, tpos ):
            result = Result( fpos, tpos )
            if result == 0:
                self.Remove( tpos )
            elif result > 0:
                self.data[tpos] = self.data[fpos]
            self.Remove( fpos )

    def CanMove( self, fpos, tpos ):
        #stay same location
        if fpos == tpos:
            return False
        #no chess to move
        if not self.data[fpos]['value']:
            return False
        #chess cannot move
        if Pos4[fpos].move == False:
            return False
        #position cannot move
        if self.GetMovable( fpos ) == False:
            return False
        #chess in tpos
        if self.data[tpos]['value'] != None:
            if self.data[tpos]['playno'] in Team4[self.data[fpos]['playno']]:
                return False
        #direct move, 1 step
        if ( OnRailway( fpos ) == ( -1, -1 ) ) | ( OnRailway( tpos ) == ( -1, -1 ) ):
            return ( tpos in Pos4[fpos].link )
        #GoBi's fly
        if Pos4[fpos]['value'] == 32:
            return tpos in self.GetFlyArea( fpos )
        #Railway
        rail, fon, ton = self.OnSameRailway( self, fpos, tpos );
        if ( fon >= 0 ) & ( ton >= 0 ):
            for i in range( fon + 1, ton ):
                if self.data[Railways[rail][i]]['value'] != None: return False
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

    def CanSelect( self, pos, playno ):
        return

    def Lost( self ):
        return False

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
        return
#get initialize position
#self.chess=...
    def Lost( self, currentMap ):
        return False
