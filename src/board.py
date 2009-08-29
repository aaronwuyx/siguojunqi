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

from Tkinter import *
from defines import *
import rule, traceback

class Board( Frame ):
    def __init__( self, master = None, **config ):
        Frame.__init__( self, master, config )
        self.pack( expand = YES, fill = BOTH )
        self.backimage = ''
        self.sepimagex = 200
        self.sepimagey = 200
        self.back = Canvas( self )
        self.back.pack()
        self.Draw_Background( '../resource/ugly2.gif' )

        self.chessw = 30
        self.chessh = 18
        self.sepwidth = 10
        self.sepheight = 10
        self.bgcolor = 'white'
        self.startx = 3 #6 to shadow?
        self.starty = 3 #6 to shadow?
        self.textfont = ( 'Courier', 9, 'bold' )
        self.pos_rectangle = {}
        self.pos_text = {}

    def Draw_Background( self, filename ):
        self.backimage = PhotoImage( file = filename )
        self.backwidth = self.backimage.width()
        self.backheight = self.backimage.height()
        self.back.create_image( self.backwidth / 2 + self.sepimagex / 2, self.backheight / 2 + self.sepimagey / 2, im = self.backimage )
        self.back.config( height = self.backheight + self.sepimagex, width = self.backwidth + self.sepimagey )
#TODO: exactly draw map...

    def Draw_Map( self, m, player ):
        for pos in range( 0, m.size ):
            self.Draw_Position( m, pos, player )

    def getPolicy( self, viewer, player, status ):
        if status == MAP_NONE:
            return False
        if status == MAP_SHOW:
            return True
        if status == MAP_HIDE:
            return ( viewer == player )
        if status == MAP_TEAM:
            try:
                p = Team4[player - 1].team.index( viewer )
                return True
            except:
                return False
        #for other status, currently return False
        return False

    def Clear_All( self ):
        self.back.delete( 'all' )
        self.pos_rectangle = {}
        self.pos_text = {}

    def Clear_Position( self, pos ):
        if self.pos_rectangle.get( pos ):
            if self.pos_rectangle[pos]:
                self.back.delete( self.pos_rectangle[pos] )
            self.pos_rectangle[pos] = None
        if self.pos_text.get( pos ):
            if self.pos_text[pos]:
                self.back.delete( self.pos_text[pos] )
            self.pos_text[pos] = None

    def Draw_Position( self, m, pos, viewer, highlight = True ):
        self.Clear_Position( pos )
        x, y, vert = self.getXY( pos )
        acbg = bg = self.bgcolor
        player = m.item[pos].getPlayer()
        status = m.item[pos].getStatus()
        show = self.getPolicy( viewer, player, status )
        if player != None:
            bg = Team4[player - 1].background
            fg = Team4[player - 1].foreground
            acbg = Team4[player - 1].activebackground
        if vert == 'V':
            self.pos_rectangle[pos] = self.back.create_rectangle( x - self.chessh / 2, y - self.chessw / 2, x + self.chessh / 2, y + self.chessw / 2, width = 2, fill = bg, activefill = acbg )
        elif vert == 'H':
            self.pos_rectangle[pos] = self.back.create_rectangle( x - self.chessw / 2, y - self.chessh / 2, x + self.chessw / 2, y + self.chessh / 2, width = 2, fill = bg, activefill = acbg )
        elif vert == 'VH':
            self.pos_rectangle[pos] = self.back.create_rectangle( x - self.chessw / 2, y - self.chessw / 2, x + self.chessw / 2, y + self.chessw / 2, width = 2, fill = bg, activefill = acbg )
        if ( player != None ) & show:
            value = m.item[pos].getValue()
            name = m.item[pos].getName()
            if vert == 'V':
            #currently i can only wrap text... to rotate it with tkinter is impossible, use gdmodule?
                self.pos_text[pos] = self.back.create_text( x, y, text = name, font = self.textfont, fill = fg, width = 1 )
            elif vert == 'H':
                self.pos_text[pos] = self.back.create_text( x, y, text = name, font = self.textfont, fill = fg )
            elif vert == 'VH':
                self.pos_text[pos] = self.back.create_text( x, y, text = name, font = self.textfont, fill = fg )

    def getXY( self, pos ):
        if ( pos >= MAXPOSITION ) | ( pos < 0 ):
            return
        xoff = self.startx + self.sepimagex / 2
        yoff = self.starty + self.sepimagey / 2
        hinc = self.chessh + self.sepheight
        winc = self.chessw + self.sepwidth
        if pos in PosV:
            if pos in PosH:
                vert = 'VH'
                xadd = self.chessw / 2
                yadd = self.chessw / 2
            else:
                vert = 'V'
                xadd = self.chessh / 2
                yadd = self.chessw / 2
        else:
            vert = 'H'
            xadd = self.chessw / 2
            yadd = self.chessh / 2
        if Pos4[pos].x < 6:
            x = xoff + xadd + Pos4[pos].x * hinc
        elif Pos4[pos].x < 11:
            x = xoff + xadd + 6 * hinc + ( Pos4[pos].x - 6 ) * winc
        else:
            x = xoff + xadd + 6 * hinc + 5 * winc + ( Pos4[pos].x - 11 ) * hinc
        if Pos4[pos].y < 6:
            y = yoff + yadd + Pos4[pos].y * hinc
        elif Pos4[pos].y < 11:
            y = yoff + yadd + 6 * hinc + ( Pos4[pos].y - 6 ) * winc
        else:
            y = yoff + yadd + 6 * hinc + 5 * winc + ( Pos4[pos].y - 11 ) * hinc
        return ( x, y, vert )

if __name__ == '__main__':
    Board().mainloop()
