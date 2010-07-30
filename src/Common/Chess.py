#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines Chess class.
"""


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

from Visible import Visible

class Chess(object):
    """
    This class describes properties of chess on board.

    Names : a list of chess names
    InitNum : number of chess when game starts
    InitRules : rule number for place chess
    MoveRules : rule number for move chess

    value - chess value
    owner - owner of chess
    visible - determines who can see the value of this chess
    """

    Names = ['', '军旗', '工兵' , '排长', '连长', '营长', '团长', '旅长', '师长', '军长', '司令', '地雷', '炸弹']
    """
        A list of chess name in Chinese.
    """
    InitNum = [0, 1, 3, 3, 3, 2, 2, 2, 2, 1, 1, 3, 2]
    """
        Chess number when initialized.
    """
    InitRules = [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]
    """
        Initialize rule, where to place the chess:
            0 - all positions
            1 - only the last two lines
            2 - all but the first line
            3 - only two unmovable places
    """
    MoveRules = [-1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    """
        Move rule, how chess behave in moving:
            0 - unmovable
            1 - normal
            2 - extended
    """

    def __init__( self, val, own, vis = Visible.VIS_SELF ):
        """
            Create a Chess by its value, owner and visibility. If the user cannot
            see the chess, its value may be unknown.
        """

        from Rule import isValidValue, isValidPlayer
        if not isValidValue( val ):
            raise ValueError( "Invalid chess value %d" % ( val ) )
        if not isValidPlayer( own ):
            raise ValueError( "Invalid player id %d" % ( own ) )
        
        self.value = val
        self.owner = own
        self.visible = vis

    def __eq__(self, other):
        if self == other:
            return True
        if type(other) != type(self):
            return False
        if (other.value == 0) or (self.value == 0):
            return False
        return (other.value == self.value) and (other.owner == self.owner)
    
    def getInitNum( self ):
        """
            Return number of this kind of chess when initialize.
        """
        return Chess.InitNum[self.value]

    def getInitRuleNum( self ):
        """
            Return rule number to apply when initialize
        """
        return Chess.InitRules[self.value]

    def getMoveRuleNum( self ):
        """
            Return rule number to apply when move
        """
        return Chess.MoveRules[self.value]

    def getName( self ):
        """
            Return chess name in Chinese
        """
        return Chess.Names[self.value]

    def __str__( self ):
        if self.value == 0:
            return "Chess: owner = %d, visible = %s" %(self.owner,self.visible)
        else:
            return "Chess: name = %s, owner = %d, visible = %s" %(self.getName(),self.owner,self.visible)

    def getOwner( self ):
        """
            Return chess owner's id
        """
        return self.owner

    def getValue( self ):
        """
            Return an integer for chess value
        """
        return self.value

    def getVisible( self ):
        """
            Return chess visibility
        """
        return self.visible

    def __hash__(self):
        return 7 * hash(self.value) + 11 * hash(self.owner)

if __name__ == '__main__':
    c1 = Chess( 2, 1, Visible.VIS_NONE )
    print( c1 )
    c2 = Chess( 5, 3 );
    print( c2 )
    print ( "initnum = %d, initrule = %d, moverule = %d, value = %d" % ( c2.getInitNum(), c2.getInitRuleNum(),
                c2.getMoveRuleNum(), c2.getValue() ) )
