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
import time

from tkinter import *
from tkinter.messagebox import showerror
import define
import profile

class Board( Frame ):
    def __init__( self, master = None, **config ):
        Frame.__init__( self, master, config )
        self.draw = Canvas( self, bg = '#eeeeee' )
        xbar = Scrollbar( self , orient = HORIZONTAL )
        ybar = Scrollbar( self )
        xbar.config( command = self.draw.xview, relief = SUNKEN )
        ybar.config( command = self.draw.yview, relief = SUNKEN )
        self.draw.config( scrollregion = ( 0, 0, 630, 630 ), xscrollcommand = xbar.set, yscrollcommand = ybar.set )
        xbar.grid( row = 1, column = 0 , sticky = EW )
        ybar.grid( row = 0, column = 1, sticky = NS )
        self.draw.grid( row = 0, column = 0, sticky = NSEW )

        self.columnconfigure( 0, weight = 1 )
        self.columnconfigure( 1, pad = 1 )
        self.rowconfigure( 0, weight = 1 )
        self.rowconfigure( 1, pad = 1 )
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
        self.tag_bg = 'background'
        self.tag_chess = 'chess'
        self.tag_dbg = 'debug'
        self.tag_chess_prefix = 'chs'
        self.tag_pos_prefix = 'pos'
        self.tag_id_prefix = 'id'
        self.selectnum = 0
        self.selectpos = -1
        self.Clear_All()

    def SetClient( self, client ):
        self.client = client
        self.board = client.map

    def Clear_All( self ):
        self.draw.delete( 'all' )

    def Draw_Background( self ):
        if os.path.exists( self.client.prof.bgfile ):
            self.bgimage = PhotoImage( file = self.client.prof.bgfile )
            bgwidth = self.bgimage.width()
            bgheight = self.bgimage.height()
            if bgwidth < 200:
                bgwidth = 200
            if bgheight < 200:
                bgheight = 200
            id = self.draw.create_image( bgwidth / 2, bgheight / 2, im = self.bgimage, tag = self.tag_bg )
        for i in range( self.board.size ):
            x1, y1 = self.GetCoordinate( i )
            for j in self.board.item[i].link:
                if i > j:
                     continue
                x2, y2 = self.GetCoordinate( j )
                id = self.draw.create_line( x1, y1, x2, y2, width = 3, fill = '#222222', tag = self.tag_bg )
            for j in self.board.item[i].rlink:
                if i > j:
                    continue
                x2, y2 = self.GetCoordinate( j )
                id = self.draw.create_line( x1, y1, x2, y2, tag = self.tag_bg )
                if self.board.item[i].IsRailway():
                    self.draw.itemconfigure( id, width = 6, fill = '#dd7777' )
                else:
                    self.draw.itemconfigure( id, width = 3, fill = '#222222' )

        for i in range( self.board.size ):
            x, y = self.GetCoordinate( i )
            if self.board.item[i].pic in [0, 2, 3, 4, 5, 6] :
                if self.board.item[i].direct == 0:
                    id = self.draw.create_rectangle( x - self.rect_height / 2, y - self.rect_width / 2 , x + self.rect_height / 2, y + self.rect_width / 2 )
                elif self.board.item[i].direct == 1:
                    id = self.draw.create_rectangle( x - self.rect_width / 2, y - self.rect_height / 2 , x + self.rect_width / 2, y + self.rect_height / 2 )
                else:
                    id = self.draw.create_rectangle( x - self.rect_width / 2, y - self.rect_width / 2 , x + self.rect_width / 2, y + self.rect_width / 2 )
            elif self.board.item[i].pic == 1:
                if self.board.item[i].direct == 0:
                    id = self.draw.create_oval( x - self.oval_height / 2, y - self.oval_width / 2 , x + self.oval_height / 2, y + self.oval_width / 2 )
                elif self.board.item[i].direct == 1:
                    id = self.draw.create_oval( x - self.oval_width / 2, y - self.oval_height / 2 , x + self.oval_width / 2, y + self.oval_height / 2 )
                else:
                    id = self.draw.create_oval( x - self.oval_width / 2, y - self.oval_width / 2 , x + self.oval_width / 2, y + self.oval_width / 2 )
            self.draw.itemconfigure( id, fill = 'white', width = 1, tag = self.tag_pos_prefix + str( i ) )
            def handler( event, self = self ):
                tg = self.draw.gettags( self.draw.find_closest( self.draw.canvasx( event.x ), self.draw.canvasy( event.y ) ) )
                for i in range( len( tg ) ):
                    k = len( self.tag_pos_prefix )
                    if tg[i][:k] == self.tag_pos_prefix:
                        try:
                            u = int( tg[i][k:] )
                        except:
                            pass
                self.SelectPos( event, u )
            self.draw.tag_bind( self.tag_pos_prefix + str( i ) , '<ButtonPress-1>', handler )
            self.draw.addtag_withtag( self.tag_bg, self.tag_pos_prefix + str( i ) )

    def Clear_Background( self ):
        self.draw.delete( self.tag_bg )

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
        self.draw.delete( self.tag_chess )

    def Clear_Pos( self, pos ):
        self.draw.delete( self.tag_chess_prefix + str( pos ) )

    def Clear_Player( self, id ):
        self.draw.delete( self.tag_id_prefix + str( id ) )

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

        if self.board.item[pos].direct == 0:
            w = Button( self.draw, text = txt, wraplength = 1 )
        elif self.board.item[pos].direct in [1, 2]:
            w = Button( self.draw, text = txt )
        w.pack()
        w.config( relief = FLAT, background = bg, foreground = fg, activebackground = acbg, font = self.text_font, command = ( lambda sp = pos: self.SelectPos( None, sp ) ) )
        if pos == self.selectpos:
            w.flash()
        if self.board.item[pos].direct == 0:
            nw = self.chess_height
            nh = self.chess_width
        elif self.board.item[pos].direct in [1, 2]:
            nw = self.chess_width
            nh = self.chess_height
        i = self.draw.create_window( x , y, window = w, width = nw, height = nh, tag = self.tag_chess_prefix + str( pos ) )
        self.draw.addtag_withtag( self.tag_id_prefix + str( id ), self.tag_chess_prefix + str( pos ) )
        self.draw.addtag_withtag( self.tag_chess, self.tag_chess_prefix + str( pos ) )
        #self.pos_pos[pos] = self.back.create_text( x + 15, y + 15, text = str( pos ), font = self.posfont, fill = '#33bb33' )

    def SelectPos( self, event, sp ):
        if self.selectnum:
            if self.board.item[sp].IsChess() :
                if self.board.item[sp].GetChess().GetPlayer() == self.client.prof.id :
                    self.selectpos = sp
                    if define.DEBUG:
                        print ( 'select pos', sp )
                    return
            self.OnMove( self.selectpos, sp )
            if define.DEBUG:
                print( 'select, move: ', self.selectpos, '->', sp )
            self.selectnum = 0
            self.selectpos = -1
        else:
            if self.board.CanSelect( sp, self.client.prof.id ):
                self.selectnum = 1
                self.selectpos = sp
                if define.DEBUG:
                    print ( 'select pos', sp )
            else:
                if define.DEBUG:
                    print ( 'cannot select pos', sp )

    def OnMove( self, fpos, tpos ):
        x1, y1 = self.GetCoordinate( fpos )
        x2, y2 = self.GetCoordinate( tpos )
        count = 12
        xinc = ( x2 - x1 ) / count
        yinc = ( y2 - y1 ) / count
        for i in range( count ):
            self.draw.move( self.tag_chess_prefix + str( fpos ) , xinc, yinc )
            self.draw.update()
            time.sleep( 0.04 )

if __name__ == '__main__':
    root = Tk()
    Board( root, None ).pack()

