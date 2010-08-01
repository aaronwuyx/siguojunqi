#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the GameRecord class.
"""

from Rule import PLAYERNUM

class GameRecord(object, player = None, layout = None, event = None, move = None):
    """
        This class defines game records.
    """
    KEYWORD = ['players','layouts','moves','events']
    #for kw in KEYWORD: kw=>self.__getattribute__[kw]
    def __init__(self):
        self.fin = False
        self.players = player
        self.layouts = layout
        self.moves = move
        if event:
            self.events = event
        else:
            self.events = []

    def fillPlayer(self, pl):
        if isinstance(pl, list) and len(pl) == PLAYERNUM:
            self.players = pl

    def fillLayout(self, la):
        if isinstance(la, list) and len(la) == PLAYERNUM:
            self.layouts = la

    def startEvent(self):
        if self.events == None:
            self.events = []
        if len(self.events) == 0:
            self.events.append(...)

