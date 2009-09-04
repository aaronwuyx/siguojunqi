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

import locale

DEBUG = True
STABLEVERSION = '0.05'
STABLESVN = '37'

MAXPLAYER = 4 #Number of players
MAXPOSITION = 129 #Number of positions
MAXCHESS = 30 #Number of pieces

POSFILENAME = 'position.txt'
POSDATA = None

#safe  : True if chess in the position cannot be removed...
#movable  : True if chess in the position can move
#pic   : 0 - rectangle 1 - oval 2 - cross 3 - castle down 4 - castle left 5 - castle up 6 - castle right
#x, y  : cursor in a map
#rail  : a list of rails pos is on
#link  : a list of nearby pos, not on railway
#raillink : a list of nearby pos on railway
#direct: 0 - vertical 1 - horizon 2 - either
class Position:

    def __init__( self, pos ):
        self.pos = pos
        self.load( pos )

    #read position settings from file
    def load( self, pos ):
        global POSDATA
        if POSDATA == None:
            POSDATA = open( POSFILENAME, 'r' ).readlines()
        line = POSDATA[pos]
        #cert:x:y:pic:movable:safe:direct:rail:link:rlink:comment
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11 = line.split( ':', 10 )
        cert = locale.atoi( a1 )
        if cert != pos:
            raise Exception( 'Invalid position data' )

        self.x = locale.atoi( a2 )
        self.y = locale.atoi( a3 )
        self.pic = locale.atoi( a4 )
        self.movable = ( locale.atoi( a5 ) != 0 )
        self.safe = ( locale.atoi( a6 ) != 0 )
        self.direct = locale.atoi( a7 )

        self.rail = []
        if a8 != '':
            for item in a8.split( ',' ):
                self.rail.append( locale.atoi( item ) )
        self.link = []
        if a9 != '':
            for item in a9.split( ',' ):
                self.link.append( locale.atoi( item ) )
        self.rlink = []
        if a10 != '':
            for item in a10.split( ',' ):
                self.rlink.append( locale.atoi( item ) )

        if DEBUG:
            print( cert, ':', self.x, self.y, self.pic, self.movable, self.safe, \
                  self.direct, self.rail, self.link, self.rlink, a11 )

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

PosH = range( 0, 30 ) + range( 60, 90 ) + range( 120, MAXPOSITION )
PosV = range( 30, 60 ) + range( 90, 120 ) + range( 120, MAXPOSITION )

#Safe Positions in a map
SafeList = [11, 13, 17, 21, 23]

#Railways : List of railways, positions in a railway is ordered 
Railways = [[5, 6, 7, 8, 9], [9, 8, 7, 6, 5], [35, 36, 37, 38, 39], [39, 38, 37, 36, 35], [65, 66, 67, 68, 69], [69, 68, 67, 66, 65], [95, 96, 97, 98, 99], [99, 98, 97, 96, 95],
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

if __name__ == '__main__':
    for i in range( MAXPOSITION ):
        Position( i )
