
from Chess import MAXVALUE
from Chess import Visible
from Player import PLAYERNUM
from Player import Player
from Position import MAXPOSITION
from Chessboard import Chessboard
from Chessboard import Railway
from Layout import Layout
from Layout import MAXCHESS

def isValidValue( value ):
    return ( value in range( MAXVALUE ) )

def isValidPlayer( player ):
    return ( player in range( PLAYERNUM ) )

def isValidPos( pos ):
    return ( pos in range( MAXPOSITION ) )

def isTeammate( player, other ):
    if not isValidPlayer( player ) or not isValidPlayer( other ):
        return False
    for p in Player.Team:
        if p == other:
            return True
    return False

def isVisible( chs, other ):
    if not isValidPlayer( other ):
        return False
    if chs.getVisible() == Visible["VIS_NONE"]:
        return False
    elif chs.getVisible() == Visible["VIS_ALL"]:
        return True
    elif chs.getVisible() == Visible["VIS_SELF"]:
        return ( other == chs.getPlayer() )
    elif chs.getVisible() == Visible["VIS_TEAM"]:
        return isTeammate( chs.getPlayer(), other )
    else:
        return False

def canSelect( c, pos, player ):
    if not isValidPlayer( player ) or not isValidPos( pos ):
        return False
    if not c.getPos( pos ).isMovable():
        return False
    if not c.getPos( pos ).isChess():
        return False
    ch = c.getChess( pos )
    if ch.getOwner() != player:
        return False
    return ( ch.getMoveRuleNum() != 0 )

def canMove( c, fpos, tpos ):
    if not isValidPos( fpos ) or not isValidPos( tpos ):
        return False
    if not c.getPos( fpos ).isMovable():
        return False
    if not c.getPos( fpos ).isChess():
        return False

    FPos = c.getPos( fpos )
    TPos = c.getPos( tpos )
    fchs = FPos.getChess()
    if fchs.getMoveRuleNum() == 0:
        return False
    if TPos.isChess():
        if TPos.isSafe():
            return False
        tchs = TPos.getChess()
        if isTeammate( tchs.getOwner(), fchs.getOwner() ):
            return False
    if not FPos.isRailway() or not TPos.isRailway():
        return ( tpos in FPos.getLink() )
    if fchs.getValue() == 2:
        return ( tpos in getFlyArea( c, fpos ) )
    for i in FPos.getRailway():
        if i in TPos.getRailway():
            Rail = Railway[i]
            fin = Rail.index( fpos )
            tin = Rail.index( tpos )
            if tin <= fin:
                continue
            for j in range( fin + 1, tin ):
                if c.getPos( Rail[j] ).isChess():
                    return False
            return True
    return False

def canMove2( c, move2 ):
    return canMove( c, move2.getFpos(), move2.getTpos() )

def result( c, fpos, tpos ):
    if not isValidPos( fpos ):
        raise ValueError( "Invalid position id %d" % ( fpos ) )
    if not isValidPos( tpos ):
        raise ValueError( "Invalid position id %d" % ( tpos ) )
    return result0( c.getChess( fpos ), c.getChess( tpos ) )

def result0( fchs, tchs ):
    if fchs == None:
        raise ValueError( "Invalid movement" )
    if tchs == None:
        return 1
    fval = fchs.getValue()
    tval = tchs.getValue()
    if not isValidValue( fval ):
        raise ValueError( "Invalid chess value %d" % ( fval ) )
    if not isValidValue( tval ):
        raise ValueError( "Invalid chess value %d" % ( tval ) )
    if ( fval == 12 ) or ( tval == 12 ):
        return 0
    if ( fval == 2 ) and ( tval == 11 ):
        return 1
    if ( fval == 10 ) and ( tval == 1 ):
        return - 1
    if fval > tval:
        return 1
    elif fval == tval:
        return 0
    else:
        return - 1

def canPlaceChessboard( c, pos, ch ):
    if not isValidPos( pos ) or not c or not ch or pos >= c.getSize():
        return False
    Pos = c.getPos( pos )
    val = ch.getValue()
    rule = ch.getInitRuleNum()
    if not isValidValue( val ):
        return False
    if Pos.isSafe():
        return False
    if pos / MAXCHESS != ch.getOwner():
        return False
    pos = pos % MAXCHESS
    if rule == 0:
        return True
    elif rule == 1:
        return ( pos < 10 )
    elif rule == 2:
        return ( pos < 25 )
    elif rule == 3:
        return ( pos in [1, 3] )
    else:
        return False

def canPlaceLayout( l, pos, ch ):
    if not isValidPos( pos ) or not l or not ch or pos >= l.getSize():
        return False
    Pos = l.getPos( pos )
    val = ch.getValue()
    rule = ch.getInitRuleNum()
    if not isValidValue( val ):
        return False
    if Pos.isSafe():
        return False
    if Pos.isChess():
        return False
    pos = pos % MAXCHESS
    if rule == 0:
        return True
    elif rule == 1:
        return ( pos < 10 )
    elif rule == 2:
        return ( pos < 25 )
    elif rule == 3:
        return ( pos in [1, 3] )
    else:
        return False

def isAlive( c, player ):
    if findJunQi( c, player ) == -1:
        return False
    for pos in range( MAXPOSITION ):
        Pos = c.getPos( pos )
        if Pos.isChess() and ( Pos.getChess().getOwner() == player ):
            for nextpos in Pos.getLink():
                if canMove( c, pos, nextpos ):
                    return True
    return False

def findJunQi( c, player ):
    pos1 = 1 + player * MAXCHESS
    pos2 = 3 + player * MAXCHESS
    if c.getPos( pos1 ).isChess():
        if c.getChess( pos1 ).getValue() == 1:
            return pos1
    if c.getPos( pos2 ).isChess():
        if c.getChess( pos2 ).getValue() == 1:
            return pos2
    return - 1

def getFlyArea( c, pos ):
    ret = []
    sel = []
    for i in range( c.getSize() ):
        ret.append( -1 )
        sel.append( False )
    if not isValidPos( pos ):
        return ret
    ret[pos] = pos
    sel[pos] = False
    flag = True
    while flag:
        flag = False
        for k in range( c.getSize() ):
            if ret[k] == k and sel[k] == False:
                flag = True
                for l in c.getPos( k ).getLinkOnRailway():
                    if ret[l] == -1:
                        ret[l] = l
                        sel[l] = c.getPos( l ).isChess()
                sel[k] = True
    return ret

def canSwap( c, pos1, pos2 ):
    if not isValidPos( pos1 ) or not isValidPos( pos2 ):
        return False
    ch1 = c.getChess( pos1 )
    ch2 = c.getChess( pos2 )

    if ( ch1 == None ) or ( ch2 == None ):
        return False
    if not canPlaceChessboard( c, pos1, ch2 ) or not canPlaceChessboard( c, pos2, ch1 ):
        return False
    return True

def isTeamAlive( c, player ):
    if not isValidPlayer( player ):
        return False
    for p in Player.Team[player]:
        if isAlive( c, p ):
            return True
    return False

def is40Alive( c, player ):
    if not isValidPlayer( player ):
        return False
    for pos in range( c.getSize() ):
        if c.getPos( pos ).isChess():
            if ( c.getChess( pos ).getOwner() == player ) and ( c.getChess( pos ).getValue() == 10 ):
                return True
    return False
