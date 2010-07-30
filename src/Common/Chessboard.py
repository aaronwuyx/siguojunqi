#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file describes ChessBoard class
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

from Positions import Positions
from Movement import Movement
from Result import Result

class ChessBoard( Positions ):
    """
        This class describes the chessboard, and provides some method to
        change chess in it.
        
        ChessBoard() : create an empty chessboard.
        removePlayer(player) : remove all chess of the player.
        move(Movement) : make a movement, return whether it succeed.
        unmove(Movement) : undo a movment, return whether it succeed.
        copyFromLayout(player, layout) : copy chess from a Layout.
    """
    
    Railway = [[5, 6, 7, 8, 9], [9, 8, 7, 6, 5], [35, 36, 37, 38, 39], [39, 38, 37, 36, 35], [65, 66, 67, 68, 69], [69, 68, 67, 66, 65], [95, 96, 97, 98, 99], [99, 98, 97, 96, 95],
          [25, 26, 27, 28, 29], [29, 28, 27, 26, 25], [55, 56, 57, 58, 59], [59, 58, 57, 56, 55], [85, 86, 87, 88, 89], [89, 88, 87, 86, 85], [115, 116, 117, 118, 119], [119, 118, 117, 116, 115],
          [5, 10, 15, 20, 25, 127, 126, 125, 89, 84, 79, 74, 69], [69, 74, 79, 84, 89, 125, 126, 127, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 121, 122, 123, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 123, 122, 121, 29, 24, 19, 14, 9],
          [99, 104, 109, 114, 119, 127, 120, 121, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 121, 120, 127, 119, 114, 109, 104, 99],
          [95, 100, 105, 110, 115, 125, 124, 123, 59, 54, 49, 44, 39], [39, 44, 49, 54, 59, 123, 124, 125, 115, 110, 105, 100, 95],
          [5, 10, 15, 20, 25, 119, 114, 109, 104, 99], [99, 104, 109, 114, 119, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 29, 24, 19, 14, 9],
          [39, 44, 49, 54, 59, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 59, 54, 49, 44, 39],
          [69, 74, 79, 84, 89, 115, 110, 105, 100, 95], [95, 100, 105, 110, 115, 89, 84, 79, 74, 69],
          [117, 126, 128, 122, 57], [57, 122, 128, 126, 117],
          [27, 120, 128, 124, 87], [87, 124, 128, 120, 27]]
    """
        a 2-dimension array of all railways. When a railway is listed,
        the one in reversed direction is also listed here.
    """
    
    def __init__( self ):
        """
            Create ChessBoard class, with extends Positions,
            setting its size to MAXPOSITION
        """
        from Rule import MAXPOSITION
        Positions.__init__( self, MAXPOSITION )
        self.step = 0
        
    def copyFromLayout( self, player, layout ):
        """
            Copy all chess in the layout, and set it in player's field.
        """
        from Rule import MAXCHESS
        self.copyFrom( layout, player * MAXCHESS )

    def move( self, m ):
        """
            This method sets chess mentioned in the Movement m.
            It checkes arguments, but it does not call Rule.canMove.
            Then this method make all necessary changes, and return
            whether the movement succeed.
        """
        if not isinstance(m, Movement):
            raise TypeError("Type mismatch, should pass in a Movement")
        if self.getStep() + 1 != m.getStep():
            print("Step doesn't match Movement!")
            return False
        fpos = m.getFromPos()
        tpos = m.getToPos() 
        result = m.getResult()
        if result == Result.RES_NON or result == None:
            print("Result should not be None")
            return False

        fchs = self.getPos(fpos).getChess()
        tchs = self.getPos(tpos).getChess()
        m.fillUndo(fchs, tchs)

        if result == Result.RES_EQU:
            self.remove( tpos )
        elif result == Result.RES_WIN:
            self.getPos(tpos).setChess(fchs)
            
        self.remove( fpos )
        self.incStep()
        return True

    def unmove(self, m):
        """
            Undo a movement, only effective when step matches, return
            whether the operation succeed.
        """
        if not isinstance(m, Movement):
            raise TypeError("Type mismatch, should pass in a Movement")
        if m.getStep() != self.getStep():
            print("Step doesn't match Movement!")
            return False
        if not m.isUndo():
            print("No undo data!");
            return False

        self.getPos(tpos).setChess(tchs)
        self.getPos(fpos).setChess(fchs)
        self.decStep()
        return True

    def removePlayer( self, player ):
        """
            Remove all one player's chess from the chessboard.
        """
        from Rule import isValidPlayer
        if not isValidPlayer( player ):
            raise ValueError( "Invalid player id %d" % ( player ) )
        for i, Pos in enumerate( self.item ):
            if Pos.isChess():
                if Pos.getChess().getOwner() == player:
                    self.remove( i )

    def getStep(self):
        """
            Return current step number.
        """
        return self.step

    def incStep(self):
        """
            Increase current step by one.
        """
        self.step = self.step + 1
        
    def decStep(self):
        """
            Decrease current step by one.
        """
        if self.step <= 0:
            raise RuntimeError("Step number has already been zero")
        self.step = self.step - 1

    def setStep(self, num):
        """
            Step step number.
        """
        if num < 0:
            raise ValueError("Step number less than zero")
        self.step = num
if __name__ == '__main__':
    from Layout import Layout
    chessBoard = ChessBoard()
    l = Layout( 0 )
    l.setToDefault()
    chessBoard.copyFromLayout( 0, l )
    mv0 = Movement(0, 29, 23, Result.RES_WIN)
    mv1 = Movement(1, 23, 17, Result.RES_WIN)
    print( chessBoard.move(mv0) )
    print( chessBoard.move(mv1) )
    print( chessBoard )
