#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines all rules in this game.
"""

from ChessBoard import ChessBoard
from Layout import Layout
from Result import Result
from Visible import Visible

#maximum player number.
MAXPLAYER = 4
#positions in a map.
MAXPOSITION = 129
#maximum positions to put chess for a layout.
MAXCHESS = 30
#total number of chess in a initialized layout.
MAXINITCHESS = 25
#maximum chess value.
MAXVALUE = 13
#4 players game teammates.
Teammate4 = [[0,2],[1,3],[0,2],[1,3]]
#2 players game teammates.
Teammate2 = [[0],[1]]
#a list of teammates. for example, TEAMMATE[0] is player 0's teammate.
TEAMMATE = Teammate4
#current player number
PLAYERNUM = MAXPLAYER

#score increase when win
SCOREUP = 3
#score decrease when lose
SCOREDOWN = 2

def isValidPlayer( player ):
    """
        verify player id.
    """
    return player >= 0 and player < PLAYERNUM

def isValidPos( pos ):
    """
        verify position number.
    """
    return pos >= 0 and pos < MAXPOSITION

def isValidValue( value ):
    """
        verify chess value.
    """
    return value >= 0 and value < MAXVALUE


def isTeammate( player, other ):
    """
        check other and player are teammates.
    """
    if not isValidPlayer( player ) or not isValidPlayer( other ):
        return False
    return other in TEAMMATE[player]

def isVisible( c, other ):
    """
        check if the chess is visible to a specified player.
    """
    if not isValidPlayer( other ):
        return False
    if c.getVisible() == Visible.VIS_NONE:
        return False
    elif c.getVisible() == Visible.VIS_ALL:
        return True
    elif c.getVisible() == Visible.VIS_SELF:
        return (other == c.getOwner())
    elif c.getVisible() == Visible.VIS_TEAM:
        return isTeammate(c.getOwner(),other)
    else:
        #unknown Visible value
        return False

def canSelect( c, pos, player ):
    """
        check if the player can select the position.
    """
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

def canMove( c, m ):
    """
        check if the player can select the position.
    """
    if type(m) != Movement:
        return False
    fpos = m.getFromPos()
    tpos = m.getToPos()
    
    #Valid pos
    if not isValidPos( fpos ) or not isValidPos( tpos ):
        return False
    #Position fpos is unmovable
    if not c.getPos( fpos ).isMovable():
        return False
    #No chess to move
    if not c.getPos( fpos ).isChess():
        return False

    FPos = c.getPos( fpos )
    TPos = c.getPos( tpos )
    fchs = FPos.getChess()

    #Chess is unmovable
    if fchs.getMoveRuleNum() == 0:
        return False

    #Chess in tpos
    if TPos.isChess():
        #Safe Position tpos
        if TPos.isSafe():
            return False
        tchs = TPos.getChess()
        #Teammate's chess
        if isTeammate( tchs.getOwner(), fchs.getOwner() ):
            return False

    #One step move
    if not FPos.isRailway() or not TPos.isRailway():
        return ( tpos in FPos.getLink() )
    #Extended movement
    if fchs.getValue() == 2:
        return ( tpos in getFlyArea( c, fpos ) )
    #Along railway
    for i in FPos.getRailway():
        if i in TPos.getRailway():
            Rail = Railway[i]
            fin = Rail.index( fpos )
            tin = Rail.index( tpos )
            if tin <= fin:
                continue
            #No other chesses on the railway
            for j in range( fin + 1, tin ):
                if c.getPos( Rail[j] ).isChess():
                    return False
            return True
    return False

def result( c, fpos, tpos ):
    """
        This method gets chess and calls result_chs.
    """
    if not isValidPos( fpos ):
        raise ValueError( "Invalid position id %d" % ( fpos ) )
    if not isValidPos( tpos ):
        raise ValueError( "Invalid position id %d" % ( tpos ) )
    return result_chs(c.getChess(fpos), c.getChess(tpos))

def result_chs( fchs, tchs ):
    """
        compare two chess and retrun results.
    """
    if fchs == None:
        raise ValueError( "Invalid movement" )
    if tchs == None:
        return Result.RES_WIN
    
    fval = fchs.getValue()
    tval = tchs.getValue()
    if not isValidValue( fval ):
        raise ValueError( "Invalid chess value %d" % ( fval ) )
    if not isValidValue( tval ):
        raise ValueError( "Invalid chess value %d" % ( tval ) )
    # ZHADAN
    if ( fval == 12 ) or ( tval == 12 ):
        return Result.RES_EQU
    # GONGBING -> DILEI
    if ( fval == 2 ) and ( tval == 11 ):
        return Result.RES_WIN
    if fval > tval:
        return Result.RES_WIN
    elif fval == tval:
        return Result.RES_EQU
    else:
        return Result.RES_LOS

def canPlace(x, pos, ch):
    if x.type == "CHESSBOARD":
        return canPlaceChessBoard(x, pos, ch)
    elif x.type == "LAYOUT":
        return canPlaceLayout(x, pos, ch)
    else:
        return False
    
def canPlaceChessBoard( c, pos, ch ):
    """
        check if chess can be placed in the specified position
        in a chessboard.
    """
    if not isValidPos( pos ) or not c or not ch or pos >= c.getSize():
        return False
    Pos = c.getPos( pos )
    val = ch.getValue()
    rule = ch.getInitRuleNum()
    
    if not isValidValue( val ):
        return False
    # Safe areas or chess already exists
    if Pos.isSafe():
        return False
    # It is my chess
    if pos / MAXCHESS != ch.getOwner():
        return False
    # Check according to InitRuleNum
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
    """
        check if chess can be placed in the specified position
        in a layout.
    """
    if not isValidPos( pos ) or not l or not ch or pos >= l.getSize():
        return False
    Pos = l.getPos( pos )
    val = ch.getValue()
    rule = ch.getInitRuleNum()
    
    if not isValidValue( val ):
        return False
    # Safe areas or chess already exists
    if Pos.isSafe():
        return False
    if Pos.isChess():
        return False
    # Check according to InitRuleNum
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
    """
        This method checks whether the specified player is alive.
    """
    # JUNQI(2) is alive
    if findJunQi( c, player ) == -1:
        return False
    # The player can move
    for Pos in c.item:
        if Pos.isChess() and Pos.getChess().getOwner() == player:
            for nextpos in Pos.getLink():
                if canMove( c, pos, nextpos ):
                    return True
    return False

def findJunQi( c, player ):
    """
        This method finds player's JUNQI on chessboard.
    """
    pos1 = 1 + player * MAXCHESS
    pos2 = 3 + player * MAXCHESS
    if c.getPos( pos1 ).isChess():
        if c.getChess( pos1 ).getValue() == 1:
            return pos1
    if c.getPos( pos2 ).isChess():
        if c.getChess( pos2 ).getValue() == 1:
            return pos2
    return -1
 
def getFlyArea( c, pos ):
    """
        This method finds all positions of GONGBING that can move to.
    """
    ret = [-1] * c.getSize()
    sel = [False] * c.getSize()
    
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
    """
        check if two chesses can swap.
    """
    if not isValidPos( pos1 ) or not isValidPos( pos2 ):
        return False
    
    ch1 = c.getChess( pos1 )
    ch2 = c.getChess( pos2 )

    if ( ch1 == None ) or ( ch2 == None ):
        return False
    if not canPlace( c, pos1, ch2 ) or not canPlace( c, pos2, ch1 ):
        return False
    
    return True

def isTeamAlive( c, player ):
    """
        check whether the game is over.
    """
    if not isValidPlayer( player ):
        return False
    for p in TEAMMATE[player]:
        if isAlive( c, p ):
            return True
    return False

def is40Alive( c, player ):
    """
        check whether the player's SILING is alive.
    """
    if not isValidPlayer( player ):
        return False
    for Pos in c.item:
        if Pos.isChess():
            if Pos.getChess().getOwner() == player and Pos.getChess().getValue == 10:
                return True
    return False

def getRoute(cb, fpos, tpos):
    """
        get a route between two positions, sometimes it does not check
        if the move is available.
    """
    if not isValidPos(fpos) or not isValidPos(tpos):
        return []

    FPos = cb.getPos(fpos)
    TPos = cb.getPos(tpos)
    if not FPos.isRailway() or not TPos.isRailway():
        # direct move
        return [fpos, tpos]
    # along railway
    for i in FPos.getRailway():
        if i in TPos.getRailway():
            Rail = cb.Railway[i]
            fin = Rail.index(fpos)
            tin = Rail.index(tpos)
            if tin < fin:
                continue
            flag = True
            # No other chesses on the railway
            for j in range(fin+1, tin):
                if cb.getPos(Rail[j]).isChess():
                    flag = False
                    break
            if flag:
                return Rail[fin:tin+1]
    # GONGBING's extended movement
    return getFlyRoute(cb, fpos, tpos)

def getFlyRoute(c, fpos, tpos):
    # Suppose Position -1 is not in Positions
    ret = [-1] * c.getSize()
    sel = [False] * c.getSize()
    ret[tpos] = tpos
    sel[tpos] = False
    flag = True
    while flag and ret[fpos] < 0:
        flag = False
        rbak = list(ret)
        for k in range(c.getSize()):
            if rbak[k] >= 0 and sel[k] == False:
                flag = True
                for l in c.getPos(k).getLinkOnRailway():
                    if ret[l] < 0:
                        ret[l] = k
                        sel[l] = c.getPos(l).isChess()
                sel[k] = True
    if ret[fpos] < 0:
        return ret
    v = [fpos]
    i = fpos
    while (v.index(ret[i]) == -1):
        i = ret[i]
        v.append(i)
    return re
    
if __name__=='__main__':
    cb = ChessBoard()
    print(getRoute(cb,5,35))
    print(getRoute(cb,5,127))
    print(getRoute(cb,5,0))
