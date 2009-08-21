from defines import *

class Map:
    def __init__( selfs, size ):
        self.data = []
        for i in range( 0, size - 1 ):
            self.data.append( {} )

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
        if self.data[pos] != {}:
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
        if self.data[pos] != {}:
            return self.data[pos]['value']

    def GetPlayer( self, pos ):
        if self.data[pos] != {}:
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
        data[pos] = {}

    def Move( self, fpos, tpos ):
        if self.CanMove( fpos, tpos ):
            result = Result( fpos, tpos )
            if result == 0:
                self.Remove( tpos )
            elif result > 0:
                self.data[tpos] = self.data[fpos]
            self.Remove( fpos )

    def CanMove( self, fpos, tpos ):
        if self.data[fpos] == {}:
            return False
        if Pos4[fpos].move == False:
            return False
        if self.GetMovable( fpos ) == False:
            return False
        return False
    """
other rules
1. hinder
2. railway
3. GoBi's fly
    """

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
    def IsLose( self ):
        return False
    def Lost40( self, currentMap ):
        return False
