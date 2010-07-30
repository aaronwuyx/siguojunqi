#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Player class.
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

from UserColor import UserColor

class Player(object):
    """
        This class provides player information, such as name, seat id, password,
        color, and other records. A connection field is also available.
    """
    PLAYERSEP = ","
    def __init__( self, name, connection = None):
        self.id = -1
        self.name = name
        self.color = None
        self.connection = connection
        self.db_id = -1
        self.pwd = None
        self.score = 0
        self.win = 0
        self.los = 0
        self.equ = 0
        self.layout = None
        self.signature = None

    def getDatabaseId(self):
        return self.db_id

    def setDatabaseId(self, id):
        self.db_id = id

    def getScore(self):
        return (self.score, self.win, self.equ, self.los)

    def setScore(self, score, win, equ, los):
        self.score = score
        self.win = win
        self.los = los
        self.equ = equ

    def getLayout(self):
        return self.layout

    def setLayout(self, lay):
        self.layout = lay

    def getSignature(self):
        return self.signature

    def setSignature(self, sign):
        self.signature = sign

    def getPwd(self):
        return self.pwd

    def setPwd(self,pwd):
        self.pwd = pwd
        
    def getName( self ):
        return self.name

    def getID( self ):
        return self.id

    def getColor(self):
        return self.color

    def setName(self, name):
        self.name = name
    
    def setID( self, id ):
        from Rule import isValidPlayer
        if isValidPlayer( id ):
            self.id = id
        else:
            raise ValueError("Inappropriate argument value of player.")

    def setColor( self, color):
        if color:
            self.color = color

    def clearID(self):
        self.id = -1

    def setConnection(self, conn):
        self.connection = conn

    def getConnection(self):
        return self.connection

    def __eq__(self, other):
        if self == other:
            return True
        if not isinstance(other, Player):
            return False
        return (self.id == other.id and self.name == other.name and
                self.color == other.color and self.pwd != other.pwd)

    def __str__(self):
        return "name: %s id: %d color: %s pwd: %s connection: %s"\
               %(self.name, self.id, self.color, self.pwd, self.connection)

    def __hash__(self):
        return 5 * hash(self.name) + 7 * hash(self.id) + \
               11 * hash(self.color) + 13 * has(self.pwd)

    def getPlayerInfo(self):
        return "%s%s%d%s%d%s%d%s%d" %(self.name, PLAYERSEP, self.win,
                                      PLAYERSEP, self.equ, PLAYERSEP,
                                      self.los, PLAYERSEP, self.score)

    def fromStringID(cls, source, id):
        # source = %color "," %name
        res = source.split(Player.PLAYERSEP, 1)
        uc = UserColor.valueOf(res[0])
        from Rule import isValidPlayer
        if not isValidPlayer(id) or not uc:
            raise ValueError("Invalid value of source %s" %(source))
        ret = Player(res[1])
        ret.setID(id)
        ret.setColor(uc)
        return ret
    
    fromStringID = classmethod(fromStringID)

    def toStringSimple(self):
        return self.toString("cn")

    def toString(self, format):
        prop = {'n':self.name,'i':self.id,'w':self.win,
                'l':self.los,'e':self.equ,'p':self.pwd,
                'd':self.db_id,'L':self.layout,'s':self.signature,
                'C':self.connection,'c':self.color}
        list = [str(prop[ch]) for ch in format if ch in prop.keys()]
        return Player.PLAYERSEP.join(list)
    
if __name__=='__main__':
    p = Player('e')
    p.setColor(UserColor.CLR_RED)
    m = p.toStringSimple()
    print( m )
    q = Player.fromStringID(m, 0)
    print( q )
    
"""
    move to gui part
    Bgcolor = ['white', '#dd2222', '#dddd22', '#22dd22', '#2222dd', '#000000', '#ffffff']
    Fgcolor = ['white', '#dddddd', '#222222', '#222222', '#dddddd', '#ffffff', '#000000']
    ActiveBgcolor = ['white', 'red', 'yellow', 'green', 'blue', 'black', 'white']
"""
