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
import rule

class Board( Frame ):
    def __init__( self, parent = None, **config ):
        Frame.__init__( self, parent, config )
        self.pack( expand = YES, fill = BOTH )
        self.backimage = ''
        self.back = Canvas( self )
        self.back.pack()
        self.Draw_Background( '../resource/ugly2.gif' )
        self.back.delete()
#    may change later?
        self.buttonwidth = 30
        self.buttonheight = 18
        self.sepwidth = 10
        self.sepheight = 10
        self.startx = 3 #6 to shadow?
        self.starty = 3 #6 to shadow?
        self.textbg = 'green'
        self.textfg = 'black'
        self.textfont = ( 'Courier', 8, 'bold' )

    def Draw_Background( self, filename ):
        self.backimage = PhotoImage( file = filename )
        self.backwidth = self.backimage.width()
        self.backheight = self.backimage.height()
        self.back.create_image( self.backwidth / 2, self.backheight / 2, im = self.backimage )
        self.back.config( height = self.backheight, width = self.backwidth )

    def Draw_Map( self, maps ):
        for pos in range( 0, maps.size ):
            self.Draw_Position( pos )
#            self.Draw_Chess( pos, maps.GetValue( pos ) )

    def Draw_Position( self, pos, highlight = False ):
        try:
            print pos
            x, y, vert = self.getXY( pos )
            if vert == 'V':
                self.back.create_rectangle( x, y, x + self.buttonheight, y + self.buttonwidth, width = 0, fill = self.textbg )
            elif vert == 'H':
                self.back.create_rectangle( x, y, x + self.buttonwidth, y + self.buttonheight, width = 0, fill = self.textbg )
            else:
                self.back.create_rectangle( x, y, x + self.buttonwidth, y + self.buttonwidth, width = 0, fill = self.textbg )
        except:
            pass

    def getXY( self, pos ):
        print 'a'
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

    def Draw_Chess( self, somedata ):
#        self.back.create_text( 50, 50, text = ' button', fill = self.textfg )
        return

    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    b = Board()
    b.Draw_Map( rule.Map( MAXPOSITION ) )
    b.run()
