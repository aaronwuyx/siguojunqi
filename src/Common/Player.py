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

from Rule import isValidPlayer

PLAYERNUM = 4 # Number of players
MAXCOLOR = 7

class Player():
    Team = [[0, 2], [1, 3], [0, 2], [1, 3]]
    Bgcolor = ['white', '#dd2222', '#dddd22', '#22dd22', '#2222dd', '#000000', '#ffffff']
    Fgcolor = ['white', '#dddddd', '#222222', '#222222', '#dddddd', '#ffffff', '#000000']
    ActiveBgcolor = ['white', 'red', 'yellow', 'green', 'blue', 'black', 'white']
    def __init__( self, name ):
        if name == '':
            self.__name = 'unknown'
        else:
            self.__name = name
        self.__id = 0
        self.__color = 0

    def getName( self ):
        return self.__name

    def getID( self ):
        return self.__id

    def setID( self, id ):
        if isValidPlayer( id ):
            self.__id = id

    def getColor( self ):
        return self.__color

    def setColor( self, color ):
        if color >= 0 and color < MAXCOLOR:
            self.__color = color

    def getBgcolor( self ):
        return self.Bgcolor[self.__color]

    def getFgcolor( self ):
        return self.Fgcolor[self.__color]

    def getActiveBgcolor( self ):
        return self.ActiveBgcolor[self.__color]

    def getTeammate( self ):
        return self.Team[self.__id]
