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

from tkinter import *
from defines import *
import rule, traceback

try:
    import Image, ImageTk
    isPIL = True
except:
    isPIL = False

class Board( Frame ):
    def __init__( self, master = None, config = Configuration() ):
        Frame.__init__( self, master )
        self.conf = config
        self.pack( expand = YES, fill = BOTH )
        self.config( relief = GROOVE, bd = 1 )
        self.back = Canvas( self )
        self.back.pack()

        if self.conf.bgfile:
            self.Draw_Background( self.conf.bgfile )

        self.chessw = 30
        self.chessh = 18
        self.sepwidth = 10
        self.sepheight = 10
        self.bgcolor = 'white'
        self.textfont = ( 'Courier', 9, 'normal' )
        self.posfont = ( 'times', 8, 'normal' )
        self.pos_rectangle = {}
        self.pos_text = {}
        self.pos_pos = {}

    def Draw_Background( self, filename ):
        if isPIL:
            self.backimage = ImageTk.PhotoImage( file = filename )
        else:
            self.backimage = PhotoImage( file = filename )
        self.backwidth = self.backimage.width()
        self.backheight = self.backimage.height()
        self.back.create_image( self.backwidth / 2 + self.conf.spacex / 2, self.backheight / 2 + self.conf.spacey / 2, im = self.backimage )
        self.back.config( height = self.backheight + self.conf.spacex, width = self.backwidth + self.conf.spacey )
#TODO: exactly draw map...

    def Draw_Map( self, m, player ):
        for pos in range( 0, m.size ):
            self.Draw_Position( m, pos, player )

    def Clear_Map( self, m ):
        for pos in range( 0, m.size ):
            self.Clear_Position( pos )

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
        self.pos_pos = {}

    def Clear_Position( self, pos ):
        if self.pos_rectangle.get( pos ):
            if self.pos_rectangle[pos]:
                self.back.delete( self.pos_rectangle[pos] )
            self.pos_rectangle[pos] = None
        if self.pos_text.get( pos ):
            if self.pos_text[pos]:
                self.back.delete( self.pos_text[pos] )
            self.pos_text[pos] = None
        if self.pos_pos.get( pos ):
            if self.pos_pos[pos]:
                self.back.delete( self.pos_pos[pos] )
            self.pos_pos[pos] = None

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
        self.pos_pos[pos] = self.back.create_text( x + 15, y + 15, text = str( pos ), font = self.posfont, fill = '#33bb33' )
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
        xoff = self.conf.offx + self.conf.spacex / 2
        yoff = self.conf.offy + self.conf.spacey / 2
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
