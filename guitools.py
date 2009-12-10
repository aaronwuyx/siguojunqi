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
except ImportError:
    from tkinter import *

def add_menuitem( menu, list ):
    for item in list:
        if item == None:
            menu.add_separator()
        elif type( item[2] ) == type( [] ):
            p = Menu( menu, tearoff = 0 )
            add_menuitem( p, item[2] )
            menu.add_cascade( label = item[0], underline = item[1], menu = p )
        else:
            menu.add_command( label = item[0], underline = item[1], command = item[2] )

def add_toolitem( parent, list, **packopt ):
    for item in list:
        m = Button( parent, text = item[0], command = item[1] )
        m.pack( packopt )
