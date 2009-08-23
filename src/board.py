# -*- coding:gb2312 -*-
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

from Tkinter import *
from defines import *
# -*- coding:gb2312 -*-
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

import rule, traceback

class Board( Frame ):
    def __init__( self, master = None, **config ):
        Frame.__init__( self, master, config )
        self.pack( expand = YES, fill = BOTH )
        self.backimage = ''
        self.back = Canvas( self )
        self.back.pack()
        self.Draw_Background( '../resource/ugly2.gif' )
#    may change later?
        self.buttonwidth = 30
        self.buttonheight = 18
        self.textwidth = self.buttonwidth / 2
        self.textheight = self.buttonheight / 2
        self.sepwidth = 10
        self.sepheight = 10
        self.bgcolor = 'white'
        self.startx = 3 #6 to shadow?
        self.starty = 3 #6 to shadow?
        self.textfont = ( 'Courier', 8, 'bold' )

    def Draw_Background( self, filename ):
        self.backimage = PhotoImage( file = filename )
        self.backwidth = self.backimage.width()
        self.backheight = self.backimage.height()
        self.back.create_image( self.backwidth / 2, self.backheight / 2, im = self.backimage )
        self.back.config( height = self.backheight, width = self.backwidth )

    def Draw_Map( self, maps ):
        for pos in range( 0, maps.size ):
            self.Draw_Position( maps, pos )

    def Draw_Position( self, maps, pos, highlight = False ):
        try:
            x, y, vert = self.getXY( pos )
            acbg = bg = self.bgcolor
            player = maps.GetPlayer( pos )
            if player != None:
                bg = bgcolor[player - 1]
                fr = frcolor[player - 1]
                acbg = acbgcolor[player - 1]
                value = maps.GetValue( pos )
            if vert == 'V':
                self.back.create_rectangle( x, y, x + self.buttonheight, y + self.buttonwidth, width = 2, fill = bg, activefill = acbg )
            elif vert == 'H':
                self.back.create_rectangle( x, y, x + self.buttonwidth, y + self.buttonheight, width = 2, fill = bg, activefill = acbg )
            else:
                self.back.create_rectangle( x, y, x + self.buttonwidth, y + self.buttonwidth, width = 2, fill = bg, activefill = acbg )
            if player != None:
                if vert == 'V':
#how to show vertically?
                    self.back.create_text( x + self.textheight, y + self.textwidth, text = maps.GetName( value ), font = self.textfont, fill = fr )
                elif vert == 'H':
                    self.back.create_text( x + self.textwidth, y + self.textheight, text = maps.GetName( value ), font = self.textfont, fill = fr )
                else:
                    self.back.create_text( x + self.textwidth, y + self.textheight, text = maps.GetName( value ), font = self.textfont, fill = fr )
        except:
            exc_info = sys.exc_info()
            print exc_info[0]
            print exc_info[1]
            traceback.print_tb( exc_info[2] )

    def getXY( self, pos ):
        if ( pos >= MAXPOSITION ) | ( pos < 0 ):
            return
        hinc = self.buttonheight + self.sepheight
        winc = self.buttonwidth + self.sepwidth
        if Pos4[pos].x < 6:
            x = self.startx + Pos4[pos].x * hinc
        elif Pos4[pos].x < 11:
            x = self.startx + 6 * hinc + ( Pos4[pos].x - 6 ) * winc
        else:
            x = self.startx + 6 * hinc + 5 * winc + ( Pos4[pos].x - 11 ) * hinc
        if Pos4[pos].y < 6:
            y = self.starty + Pos4[pos].y * hinc
        elif Pos4[pos].y < 11:
            y = self.starty + 6 * hinc + ( Pos4[pos].y - 6 ) * winc
        else:
            y = self.starty + 6 * hinc + 5 * winc + ( Pos4[pos].y - 11 ) * hinc
        if pos in PosV:
            if pos in PosH:
                return ( x, y, 'VH' )
            else:
                return ( x, y, 'V' )
        else:
            return ( x, y, 'H' )
