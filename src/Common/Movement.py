#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Movement class.
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

from Result import Result

class Movement(object):
    """
        This class describes a chess movement. It stores information about
        positions, chess and its result.

        flag : not used now
        step : step number
        fpos : position number from
        tpos : position number to
        result : result of the move
        undo : whether undo info is available
        fchs : chess from
        tchs : chess to
    """

    MOVESEP = ','
    def getResult(self):
        return self.result

    def setResult(self,res):
        self.result = res

    def getFromPos(self):
        return self.fpos

    def getToPos(self):
        return self.tpos

    def getStep(self):
        return self.step

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag

    def __init__( self, astep, afpos, atpos, aresult = Result.RES_NON, aflag = 0):
        from Rule import isValidPos
        if not isValidPos( afpos ):
            raise ValueError( "Invalid position id %d" % ( afpos ) )
        if not isValidPos( atpos ):
            raise ValueError( "Invalid position id %d" % ( atpos ) )
        if astep < 0:
            raise ValueError( "Invalid step number %d" % ( astep ) )
        self.step = astep
        self.fpos = afpos
        self.tpos = atpos
        self.flag = aflag
        self.result = aresult
        self.undo = False
        self.fchs = None
        self.tchs = None

    def toString( self ):
        return "%d%s%d%s%d%s%d%s%s" % (self.step, Movement.MOVESEP,
                                         self.fpos, Movement.MOVESEP,
                                         self.tpos, Movement.MOVESEP,
                                         self.flag, Movement.MOVESEP,
                                         self.result)
    def fromString( cls, source ):
        sp = source.split(Movement.MOVESEP)
        if len(sp) != 5:
            raise ValueError( "Invalid syntax of Movement %s" %(source))
        step = int(sp[0].strip())
        fpos = int(sp[1].strip())
        tpos = int(sp[2].strip())
        flag = int(sp[3].strip())
        result = Result.valueOf(sp[4].strip())
        return Movement(step,fpos,tpos,result,flag)

    fromString = classmethod(fromString)
    
    def fillUndo(self, fchs, tchs):
        if self.result == Result.RES_NON or self.result == None:
            raise RuntimeError( "Try to fill undo data while result is unknown")
        self.fchs = fchs
        self.tchs = tchs
        self.undo = True

    def isUndo(self):
        return self.undo

    def getFromChs(self):
        return self.fchs

    def getToChs(self):
        return self.tchs

    def __str__(self):
        return self.toString()
    
if __name__=='__main__':
    mv = Movement.fromString('1,3,5,0,RES_NON')
    print(mv)
    mv1 = Movement.fromString(mv.toString())
    print(mv1)
