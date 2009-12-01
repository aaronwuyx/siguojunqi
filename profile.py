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
import pickle # use pickle.Pickler to dump data 

import define

#constants
PROFILEVER = 1 # identify different profiles

class Profile:

    Bgcolor = ['#dd2222', '#dddd22', '#22dd22', '#2222dd']
    Fgcolor = ['#dddddd', '#222222', '#222222', '#dddddd']
    ActiveBgcolor = ['red', 'yellow', 'green', 'blue']
    Team = [[0, 2], [1, 3]]

    def __init__( self, name ):
        if name == '':
            name = 'default'
        self.name = name #identify player
        self.filename = self.name + '.cfg'
        self.pfver = PROFILEVER
        self.init() #initialize settings

    def init( self ):
        # set default value for rest of attributions
        self.setid( 0 ) #default id is 0
        self.bgfile = 'blank.gif' #background is white 

        self.lineupfile = '' #load lineup from file
        self.lineup = define.Lineup( self.id )
        self.lineup.SetToDefault()

        self.win = 0
        self.total = 0

    def setid( self, idnum ):
        #validate idnum
        if idnum >= define.MAXPLAYER | idnum < 0:
            return

        self.id = idnum
        self.bg = Profile.Bgcolor[idnum]
        self.fg = Profile.Fgcolor[idnum]
        self.acbg = Profile.ActiveBgcolor[idnum]
        self.teammate = Profile.Team[idnum % 2]

    def load( self ):
        #open file in read mode
        try:
            f = open( self.filename, 'r' )
        except:
            if define.log_lv & define.LOG_DEF:
                exc_info = sys.exc_info()
                print( exc_info[0], '\n', exc_info[1] )
                traceback.print_tb( exc_info[2] )
            return

        #use pickle to load info
        p = pickle.Unpickler( f )

        try:
            obj = p.load()
            self.dump_from( obj )
        except TypeError:
            return

        #close the file
        try:
            f.close()
        except:
            pass

        #automatically sync with lineup file
        if self.lineupfile:
            self.loadlineup()

    def dump_from( self, obj ):
        #check data type
        for key in obj.__dict__.keys():
            if not key in self.__dict__.keys():
                raise TypeError( "Invalid type" )

        #dump data
        for key in obj.__dict__.keys():
            self.__dict__[key] = obj.__dict__[key]

    def loadlineup( self ):
        try:
            new = define.Lineup( self.id )
            new.Load( self.lineupfile )
            self.lineup = new
        except:
            print ( 'cannot load file' )

    def savelineup( self ):
        try:
            self.lineup.Save( self.lineupfile )
        except:
            print ( 'cannot load file' )

    def save( self ):
        try:
            f = open( self.filename, 'w' )
        except IOError:
            if define.DEBUG:
                exc_info = sys.exc_info()
                print( exc_info[0], '\n', exc_info[1] )
                traceback.print_tb( exc_info[2] )
            return

        #use pickle to load info
        p = pickle.Pickler( f )
        try:
            p.dump( self )
        except pickle.PickleError:
            return

        #close the file
        try:
            f.close()
        except:
            pass

        #if necessary, update the lineup file
        if self.lineupfile:
            self.savelineup()

    def __str__( self ):
        return str( self.__dict__ )

if __name__ == '__main__':
    p = Profile( 'sean' )
    print( p )
    p.save()
    p.bg = '333'
    print ( p )
    p.load()
    print ( p )
