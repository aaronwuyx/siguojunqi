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

from tkinter import *
from tkinter.messagebox import showerror
import define
import profile

class Board( Frame ):
    def __init__( self, master = None, **config ):
        Frame.__init__( self, master, config )
        self.draw = Canvas( self, bg = '#eeeeee', width = 630, height = 630 )
        xbar = Scrollbar( master , orient = HORIZONTAL )
        ybar = Scrollbar( master )
        xbar.pack( side = BOTTOM, expand = YES, fill = X )
        ybar.pack( side = RIGHT, expand = YES, fill = Y )
        self.draw.pack()
        xbar.config( command = self.draw.xview, relief = SUNKEN )
        ybar.config( command = self.draw.yview, relief = SUNKEN )
        self.draw.config( xscrollcommand = xbar.set, yscrollcommand = ybar.set )

        self.init()

    def init( self ):
        self.chess_width = 32
        self.chess_height = 18
        self.rect_width = 26
        self.rect_height = 14
        self.oval_width = 36
        self.oval_height = 20
        self.space_width = 42
        self.space_height = 28
        self.offset_x = 50
        self.offset_y = 50

        self.text_font = ( 'Courier', 9, 'normal' )
        self.inst_font = ( 'Times', 8, 'normal' )
        self.client = None
        self.board = None

        self.Clear_All()

    def Clear_All( self ):
        self.draw.delete( 'all' )
        self.back = []
        self.inst = []
        self.text = {}
        self.rect = {}

    def SetClient( self, client ):
        self.client = client
        self.board = client.map

    def Draw_Background( self ):
        if os.path.exists( self.client.prof.bgfile ):
            self.bgimage = PhotoImage( file = self.client.prof.bgfile )
            bgwidth = self.bgimage.width()
            bgheight = self.bgimage.height()
            if bgwidth < 200:
                bgwidth = 200
            if bgheight < 200:
                bgheight = 200
            id = self.draw.create_image( bgwidth / 2, bgheight / 2, im = self.bgimage )
            self.back.append( id )
        for i in range( self.board.size ):
            x1, y1 = self.GetCoordinate( i )
            for j in self.board.item[i].link:
                if i > j:
                     continue
                x2, y2 = self.GetCoordinate( j )
                id = self.draw.create_line( x1, y1, x2, y2, width = 3, fill = '#222222' )
                self.back.append( id )
            for j in self.board.item[i].rlink:
                if i > j:
                    continue
                x2, y2 = self.GetCoordinate( j )
                if self.board.item[i].IsRailway():
                    id = self.draw.create_line( x1, y1, x2, y2, width = 6, fill = '#dd7777' )
                else:
                    id = self.draw.create_line( x1, y1, x2, y2, width = 3, fill = '#222222' )
                self.back.append( id )
        for i in range( self.board.size ):
            x, y = self.GetCoordinate( i )
            if self.board.item[i].pic in [0, 2, 3, 4, 5, 6] :
                if self.board.item[i].direct == 0:
                    id = self.draw.create_rectangle( x - self.rect_height / 2, y - self.rect_width / 2 , x + self.rect_height / 2, y + self.rect_width / 2, width = 1, fill = 'white' )
                elif self.board.item[i].direct == 1:
                    id = self.draw.create_rectangle( x - self.rect_width / 2, y - self.rect_height / 2 , x + self.rect_width / 2, y + self.rect_height / 2, width = 1, fill = 'white' )
                else:
                    id = self.draw.create_rectangle( x - self.rect_width / 2, y - self.rect_width / 2 , x + self.rect_width / 2, y + self.rect_width / 2, width = 1, fill = 'white' )
                self.back.append( id )
            elif self.board.item[i].pic == 1:
                if self.board.item[i].direct == 0:
                    id = self.draw.create_oval( x - self.oval_height / 2, y - self.oval_width / 2 , x + self.oval_height / 2, y + self.oval_width / 2, width = 1, fill = 'white' )
                elif self.board.item[i].direct == 1:
                    id = self.draw.create_oval( x - self.oval_width / 2, y - self.oval_height / 2 , x + self.oval_width / 2, y + self.oval_height / 2, width = 1, fill = 'white' )
                else:
                    id = self.draw.create_oval( x - self.oval_width / 2, y - self.oval_width / 2 , x + self.oval_width / 2, y + self.oval_width / 2, width = 1, fill = 'white' )
                self.back.append( id )

    def Clear_Background( self ):
        for item in self.back:
            self.draw.delete( item )
        self.back = []

    def GetCoordinate( self, pos ):
        if ( pos >= self.client.map.size ) | ( pos < 0 ):
            return
        x = self.offset_x
        y = self.offset_y
        if self.board.item[pos].direct == 0:
            x = x + self.chess_height / 2
            y = y + self.chess_width / 2
        elif self.board.item[pos].direct == 1:
            x = x + self.chess_width / 2
            y = y + self.chess_height / 2
        else:
            x = x + self.chess_width / 2
            y = y + self.chess_width / 2

        vx = self.board.item[pos].x
        vy = self.board.item[pos].y
        if vx < 6:
            x += vx * self.space_height
        else:
            x += 6 * self.space_height
            if vx < 11:
                x += ( vx - 6 ) * self.space_width
            else:
                x += 5 * self.space_width + ( vx - 11 ) * self.space_height
        if vy < 6:
            y += vy * self.space_height
        else:
            y += 6 * self.space_height
            if vy < 11:
                y += ( vy - 6 ) * self.space_width
            else:
                y += 5 * self.space_width + ( vy - 11 ) * self.space_height
        return ( x, y )

    def Draw_Chess( self ):
        for i in range( self.board.size ):
            self.Draw_Pos( i )

    def Clear_Chess( self ):
        for pos in self.text.keys():
            self.draw.delete( self.text[pos] )
        self.text = {}

    def Clear_Pos( self, pos ):
        if pos in self.text.keys():
            self.draw.delete( self.text.pop( pos ) )

    def Draw_Pos( self, pos ):
        self.Clear_Pos( pos )
        if self.board.item[pos].IsChess() == False:
            return
        x, y = self.GetCoordinate( pos )
        c = self.board.item[pos].chess
        if c.IsVisible( self.client.prof.id ):
            txt = c.GetName()
        else:
            txt = '　　'
        id = c.GetPlayer()
        bg = profile.Profile.Bgcolor[id]
        fg = profile.Profile.Fgcolor[id]
        acbg = profile.Profile.ActiveBgColor[id]
        def notdone():
            showerror( 'Error', 'Function not implemented' )

        if self.board.item[pos].direct == 0:
            w = Button( self.draw, text = txt, wraplength = 1 )
        elif self.board.item[pos].direct in [1, 2]:
            w = Button( self.draw, text = txt )
        w.pack()
        w.config( relief = FLAT, background = bg, foreground = fg, activebackground = acbg, font = self.text_font, command = notdone )
        if self.board.item[pos].direct == 0:
            id = self.draw.create_window( x , y, window = w, width = self.chess_height, height = self.chess_width )
        elif self.board.item[pos].direct in [1, 2]:
            id = self.draw.create_window( x , y, window = w, height = self.chess_height, width = self.chess_width )
        self.text[pos] = id
"""
        self.pos_pos[pos] = self.back.create_text( x + 15, y + 15, text = str( pos ), font = self.posfont, fill = '#33bb33' )
"""

if __name__ == '__main__':
    root = Tk()
    Board( root, None ).pack()

