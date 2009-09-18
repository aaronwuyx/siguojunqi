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
import traceback
import define

class Profile:

    Bgcolor = ['#dd2222', '#dddd22', '#22dd22', '#2222dd']
    Fgcolor = ['#dddddd', '#222222', '#222222', '#dddddd']
    ActiveBgColor = ['red', 'yellow', 'green', 'blue']
    Team = [[0, 2], [1, 3]]

    def __init__( self, name ):
        if name == '':
            name = 'default'
        self.name = name #identify himself from other players
        self.filename = self.name + '.cfg'
        self.init() #initialize settings

    def init( self ):
        self.id = 0
        self.bg = Profile.Bgcolor[self.id]
        self.fg = Profile.Fgcolor[self.id]
        self.acbg = Profile.ActiveBgColor[self.id]
        self.teammate = Profile.Team[self.id % 2]

        self.host = 'localhost'
        self.port = define.DEFAULTPORT

        self.bgfile = 'blank.gif'
        self.lineupfile = ''
        self.lineup = None

        self.win = 0
        self.total = 0


    def load( self ):
        try:
            f = open( self.filename, 'r' )
        except:
            if define.log_lv & define.LOG_DEF:
                exc_info = sys.exc_info()
                print( exc_info[0], '\n', exc_info[1] )
                traceback.print_tb( exc_info[2] )
            return

        for line in f.readlines():
            try:
                key, value = line.split( '=', 1 )
                key = key.strip()
                value = value.strip()
                if key == 'name':
                    if self.name != value:
                        break
                if key == 'id':
                    self.id = int( value )

                if key == 'bgfile':
                    if os.path.sep == '/':
                        value = value.replace( '\\', '/' )
                    elif os.path.sep == '\\':
                        value = value.replace( '/', '\\' )
                    if os.path.exists( value ):
                        self.bgfile = value
                if key == 'lineup':
                    if os.path.sep == '/':
                        value = value.replace( '\\', '/' )
                    elif os.path.sep == '\\':
                        value = value.replace( '/', '\\' )
                    if os.path.exists( value ):
                        self.lineupfile = value

                if key == 'host':
                    self.host = value
                if key == 'port':
                    self.port = int( value )

                if key == 'bg':
                    self.bg = value
                if key == 'fg':
                    self.fg = value
                if key == 'acbg':
                    self.acbg = value

            except:
                pass
                #if define.DEBUG:
                #    exc_info = sys.exc_info()
                #    print( exc_info[0], '\n', exc_info[1] )
                #    traceback.print_tb( exc_info[2] )

        try:
            f.close()
        except:
            pass
        self.loadlineup()

    def loadlineup( self ):
        bak = self.lineup
        self.lineup = define.Lineup( self.id )
        if self.lineupfile != '':
            self.lineup = define.Lineup( self.id )
            try:
                self.lineup.Load( self.lineupfile )
            except:
                if bak:
                    self.lineup = bak
                else:
                    self.lineupfile = ''
                    self.lineup.SetToDefault()
        else:
            self.lineup.SetToDefault()

    def save( self ):
        try:
            f = open( self.filename, 'w' )
        except:
            if define.DEBUG:
                exc_info = sys.exc_info()
                print( exc_info[0], '\n', exc_info[1] )
                traceback.print_tb( exc_info[2] )
            return
        f.write( 'Siguo game profile :\n' )
        f.write( 'name = ' + self.name + '\n' )
        f.write( 'id = ' + str( self.id ) + '\n' )

        f.write( 'lineup = ' + self.lineupfile + '\n' )
        f.write( 'bgfile = ' + self.bgfile + '\n' )

        f.write( 'host = ' + self.host + '\n' )
        f.write( 'port = ' + str( self.port ) + '\n' )

        f.write( 'bg = ' + self.bg + '\n' )
        f.write( 'fg = ' + self.fg + '\n' )
        f.write( 'acbg = ' + self.acbg + '\n' )

        try:
            f.close()
        except:
            pass

#       self.place = GetDefaultPlace( self.player )

if __name__ == '__main__':
    pass
