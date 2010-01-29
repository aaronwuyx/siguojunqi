#!/usr/bin/python
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

from Position import Position
from Chess import Chess
from Chess import Visible
from Positions import Positions
from Chessboard import Chessboard
from Layout import Layout
from Layout import fromString as Layout_fromString
from Layout import load as Layout_load
from Rule import *
from Movement1 import Movement1
from Movement1 import fromString as Movement1_fromString
from Movement2 import Movement2
from Movement2 import fromString as Movement2_fromString

STABLEVERSION = '0.09'
STABLESVN = '85'
ChangeLog = ''

from Chess import MAXINITCHESS
from Chess import MAXVALUE
from Position import MAXPOSITION
from Layout import MAXCHESS
from Player import PLAYERNUM as MAXPLAYER
from Player import PLAYERNUM
