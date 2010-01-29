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

MAXINITCHESS = 25 # Number of pieces
MAXVALUE = 13 # Maximum chess value

#values set to Chess.visible
Visible = {"VIS_NONE":0, "VIS_SELF":1, "VIS_TEAM":2, "VIS_ALL":3}

class Chess:
    """
    This class describes attributions of Chess
    
    Class Chess():
        value - chess value identifier
        name - chess name according to its value
        initnum -  chess number when game starts
        initrule - restruction number that decides its position when game starts
        moverule - restruction of movement
        player - player id of player the belongs to
        visible - the chess's visible mode
    """

    Names = ["", '军旗', '工兵' , '排长', '连长', '营长', '团长', '旅长', '师长', '军长', '司令', '地雷', '炸弹']
    InitNum = [0, 1, 3, 3, 3, 2, 2, 2, 2, 1, 1, 3, 2]
    InitRules = [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]
    MoveRules = [-1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]

    def __init__( self, value, player, visible = Visible["VIS_SELF"] ):
        from Rule import isValidValue, isValidPlayer

        if not isValidValue( value ):
            raise ValueError( "Invalid chess value %d" % ( value ) );
        if not isValidPlayer( player ):
            raise ValueError( "Invalid player id %d" % ( player ) );

        self.__value = value
        self.__player = player
        self.__visible = visible

        if value:
            self.__name = Chess.Names[value]
            self.__initnum = Chess.InitNum[value]
            self.__initrule = Chess.InitRules[value]
            self.__moverule = Chess.MoveRules[value]

        #logging.info( self.__str__() )

    def __str__( self ):
        return str( self.__dict__ )

    def getOwner( self ):
        return self.__player

    def getValue( self ):
        return self.__value

    def getVisible( self ):
        return self.__visible

    def getName( self ):
        return self.__name

    def getInitNum( self ):
        return self.__initnum

    def getInitRuleNum( self ):
        return self.__initrule

    def getMoveRuleNum( self ):
        return self.__moverule

if __name__ == '__main__':
    c1 = Chess( 2, 1, Visible["VIS_NONE"] )
    print( c1 )
    c2 = Chess( 5, 3 );
    print( c2 )
    print ( "%d,%d,%d,%d" % ( c2.getInitNum(), c2.getInitRuleNum(),
                c2.getMoveRuleNum(), c2.getValue() ) );
