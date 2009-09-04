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

import os
import sys
import define

class Profile:

    Bgcolor = ['#dd2222', '#dddd22', '#22dd22', '#2222dd']
    Fgcolor = ['#dddddd', '#222222', '#dddddd', '#222222']
    ActiveBgColor = ['red', 'yellow', 'green', 'blue']
    Team = [[0, 2], [1, 3]]

    def __init__( self, id, name ):

        if ( id >= define.MAXPLAYER ) or ( id < 0 ):
            id = 0
        if name == '':
            name = 'Unknown'

        self.id = id #0..3
        self.name = name #identify himself from other players
        self.bg = Profile.Bgcolor[id]
        self.fg = Profile.Fgcolor[id]
        self.acbg = Profile.ActiveBgColor[id]
        self.teammate = Team[id % 2]
        self.init() #initialize settings
        self.load() #load customed settings
        self.save() #immediately save settings, for future reload

"""
#defined in MapItem.status
MAP_NONE = 'None' #Nobody | Nothing
MAP_HIDE = 'Hide' #Player himself can see the chess
MAP_TEAM = 'Team' #Player & his teammate can see the chess
MAP_OTHER = 'Other' #Not defined... reserved for stander-by...
MAP_SHOW = 'Show' #Everyone can see it, to ease debug...

#MapItem is items used in class Map | something called a "Placement"
#it represents an empty position or pieces in the position
class MapItem:
    def __init__( self, value = None, player = None, status = MAP_NONE ):
        self.value = value
        self.player = player
        self.status = status
    def getValue( self ):
        return self.value
    def getPlayer( self ):
        return self.player
    def getStatus( self ):
        return self.status
    def getName( self ):
        if self.value == None:
            return
        return GetChessName( self.value )
    def getRule( self ):
        if self.value == None:
            return
        return GetChessRule( self.value )
    def getMove( self ):
        if self.value == None:
            return
        return GetChessMove( self.value )

#a class on properties of chess 
class ChessProp:
    def __init__( self, name, value, initnum, rule = 0, move = 1 ):
        self.name = name #In Chinese
        self.value = value
        self.initnum = initnum #Number of this kind of chess when initialized
        self.rule = rule #Rule of placement
        self.move = move #Rule of movement

#And here is the data
InitChess = [ChessProp( '司令', 40, 1 ), ChessProp( '军长', 39, 1 ), ChessProp( '师长', 38, 2 ), ChessProp( '旅长', 37, 2 ),
             ChessProp( '团长', 36, 2 ), ChessProp( '营长', 35, 2 ), ChessProp( '连长', 34, 3 ), ChessProp( '排长', 33, 3 ),
             ChessProp( '工兵', 32, 3, 0, 2 ), ChessProp( '地雷', 41, 3, 1, 0 ), ChessProp( '炸弹', 42, 2, 2 ), ChessProp( '军旗', 31, 1, 3, 0 )]

#GetChessxxx : find "value" through InitChess and get the corresponding attribute, None if not found...
def GetChessName( value ):
    for prop in InitChess:
        if prop.value == value:
            return prop.name

def GetChessRule( value ):
    for prop in InitChess:
        if prop.value == value:
            return prop.rule

def GetChessMove( value ):
    for prop in InitChess:
        if prop.value == value:
            return prop.move

def GetChessInit( value ):
    for prop in InitChess:
        if prop.value == value:
            return prop.initnum

#Generate default placement
def GetDefaultPlace( player, status = MAP_HIDE ):
    return [MapItem( 41, player, status ), MapItem( 31, player, status ), MapItem( 41, player, status ), MapItem( 33, player, status ),
           MapItem( 36, player, status ), MapItem( 33, player, status ), MapItem( 41, player, status ), MapItem( 36, player, status ),
           MapItem( 32, player, status ), MapItem( 33, player, status ), MapItem( 37, player, status ), MapItem(),
           MapItem( 34, player, status ), MapItem(), MapItem( 37, player, status ), MapItem( 40, player, status ),
           MapItem( 35, player, status ), MapItem(), MapItem( 35, player, status ), MapItem( 39, player, status ),
           MapItem( 42, player, status ), MapItem(), MapItem( 34, player, status ), MapItem(),
           MapItem( 42, player, status ), MapItem( 38, player, status ), MapItem( 32, player, status ),
           MapItem( 34, player, status ), MapItem( 32, player, status ), MapItem( 38, player, status )]

class Configuration:
    def __init__( self ):
        self.name = 'Unknown'
        self.player = 1
        self.placefile = 'place.cfg'
        self.place = GetDefaultPlace( self.player )
        self.host = 'localhost'
        self.port = 30000

        self.bgfile = '..' + os.sep + 'resource' + os.sep + 'ugly2.gif'
        self.spacex = 200
        self.spacey = 200
        self.offx = 3 #6 to have shadow?
        self.offy = 3

    def config( self ):
        return

    def Load( self, filename ):
        try:
            f = open( filename, 'r' )
        except:
            return
        for line in f.readlines():
            try:
                key, value = line.split( '=' , 1 )
                key = key.strip()
                value = value.strip()
                if key == 'name':
                    self.name = value
                if key == 'bgfile':
                    try:
                        self.bgfile = value
                    except:
                        pass
                if key == 'player':
                    try:
                        self.player = string.atoi( value )
                    except:
                        pass
                if key == 'place':
                    self.placefile = value
                if key == 'host':
                    self.host = value
                if key == 'port':
                    try:
                        self.port = string.atoi( value )
                    except:
                        pass
                if key == 'space':
                    try:
                        xs, ys = value.split( ',' )
                        x = string.atoi( xs )
                        y = string.atoi( ys )
                        self.spacex = x
                        self.spacey = y
                    except:
                        pass
                if key == 'offset':
                    try:
                        xs, ys = value.split( ',' )
                        x = string.atoi( xs )
                        y = string.atoi( ys )
                        self.offx = x
                        self.offy = y
                    except:
                        pass
            except:
                pass
        try:
            f.close()
        except:
            pass
        backfile = self.placefile
        backplace = self.place
        if self.loadPlace( self.placefile ):
            if not ( rule.CheckPlace1( self.place ) & rule.CheckPlace2( self.place ) ):
                self.placefile = backfile
                self.place = backplace
        else:
            self.placefile = backfile
            self.place = backplace

    def Save( self, filename ):
        try:
            f = open( filename, 'w' )
        except:
            return
        f.write( 'siguo game client configuration:\n' )
        f.write( '\nclient\n' )
        f.write( 'name=%s\n' % ( self.name ) )
        f.write( 'player=%d\n' % ( self.player ) )
        f.write( 'place=%s\n' % ( self.placefile ) )
        f.write( 'host=%s\n' % ( self.host ) )
        f.write( 'port=%d\n' % ( self.port ) )
        f.write( '\nboard\n' )
        f.write( 'bgfile=%s\n' % ( self.bgfile ) )
        f.write( 'offset=%d,%d\n' % ( self.offx, self.offy ) )
        f.write( 'space=%d,%d\n' % ( self.spacex, self.spacey ) )
        try:
            f.close()
        except:
            pass
        self.savePlace( self.placefile )

    def loadPlace( self, filename ):
        try:
            f = open ( filename, 'r' )
        except:
            return
        place = []
        for line in f.readlines():
            for item in line.split():
                try:
                    if item == 'None':
                        place.append( MapItem() )
                    else:
                        place.append( MapItem( string.atoi( item ), self.player , MAP_HIDE ) )
                except:
                    return
        return place

    def savePlace( self, filename ):
        try:
            f = open( filename, 'w' )
        except:
            return False
        for place in self.place:
            f.write( str( place.getValue() ) + ' ' )
        f.write( '\n' )
        return True

if __name__ == '__main__':
    for i in range( len( Pos4 ) ):
        print Pos4[i]
"""
