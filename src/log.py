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

try:
    from Tkinter import *
except:
    from tkinter import *

class TextOutput( Frame ):
    def __init__( self, master = None, **config ):
        Frame.__init__( self, master, config )
        self.text = Text( self, bg = 'white', relief = RIDGE, bd = 1 )
        sbar = Scrollbar( self )
        self.text.config( yscrollcommand = sbar.set )
        sbar.config( command = self.text.yview )
        sbar.pack( side = RIGHT, expand = YES, fill = Y )
        self.text.pack( side = TOP , expand = YES, fill = BOTH )

    def write( self, text ):
        self.text.insert( END, str( text ) )
        self.text.see( END )
        self.text.update()

    def writelines( self, lines ):
        for line in lines:
            self.write( line )

if __name__ == '__main__':
    t = Tk()
    import sys
    tmp = sys.stdout
    p = TextOutput( t )
    p.pack()
    sys.stdout = p
    print( 'a' )
    t.mainloop()
    sys.stdout = tmp
