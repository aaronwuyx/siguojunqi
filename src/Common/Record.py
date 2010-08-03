#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the GameRecord class.
"""

from Rule import PLAYERNUM

class RecordEvent(object):
    """
        This class defines RecordEvent class.
    """
    EVENTTYPES = ["INIT","PLACE","MOVE","EXIT","FINI"]
    ARGSEP = ","
    def __init__(self, types, value = None):
        if not types in RecordEvent.EVENTTYPES:
            raise ValueError("Invalid type of RecordEvent: %s" %types)
        self.types = types
        self.value = value

    def fromString(cls, source):
        s = source.split(RecordEvent.ARGSEP,1)
        if len(s) == 1:
            if s[0].strip() in ['INIT', 'FINI']:
                return RecordEvent(s[0].strip())
        elif len(s) == 2:
            if s[0].strip() in ['PLACE', 'MOVE', 'EXIT']:
                return RecordEvent(s[0].strip(), int(s[1].strip()))
        raise ValueError("Invalid source syntax for RecordEvent: %s" %source)
    fromString=classmethod(fromString)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def getTypes(self):
        return self.types

    def __str__(self):
        if self.types in ["INIT", "FINI"]:
            return self.types
        elif self.types in ["PLACE", "MOVE", "EXIT"]:
            return self.types + RecordEvent.ARGSEP + str(self.value)
        else:
            return None

class GameRecord(object, player = None, layout = None, event = None, move = None):
    """
        This class defines game records.
    """
    KEYWORD = ['players','layouts','moves','events']
    #for kw in KEYWORD: kw=>self.__getattribute__[kw]
    def __init__(self):
        if player and len(player) != PLAYERNUM:
            raise ValueError("Invalid Player list")
        if layout and len(layout) != PLAYERNUM:
            raise ValueError("Invalid Layout list")
        self.fin = False
        self.players = list(player)
        if layout:
            self.layouts = list(layout)
        else:
            self.layouts = [None]*PLAYERNUM

        self.moves = list(move)
        if event:
            self.events = list(event)
        else:
            self.events = []

    def _fillPlayer(self, pl):
        if isinstance(pl, list) and len(pl) == PLAYERNUM:
            self.players = pl
            return True
        return False

    def fillLayout(self, la):
        if isinstance(la, list) and len(la) == PLAYERNUM:
            self.layouts = la
            return True
        return False

    def startRecord(self, player):
        if len(self.events) > 0:
            print('Warning: INIT event is not the first one')
        self.events.append(RecordEvent('INIT'))
        self._fillPlayer(player)

    def stopRecord(self):
        self.events.append(RecordEvent('FINI'))
        self.fin = True

    def recordMove(self, movement):
        from Movement import Movement
        if not isinstance(movement,Movement):
            raise ValueError("You should specify a Movement here")
        self.moves.append(movement)
        p = len(self.moves) - 1
        self.events.append(RecordEvent('MOVE',p))

    def recordExit(self, id):
        from Rule import isValidPlayer
        if not isValidPlayer(id):
            raise ValueError("Player id is invalid")
        self.events.append(RecordEvent('EXIT',id))

    def recordLayout(self, id, lay):
        from Rule import isValidPlayer
        if not isValidPlayer(id):
            raise ValueError("Player id is invalid")
        if self.layouts[id]:
            print("Warning: Layout data already exist, overlay it")
        self.events.append(RecordEvent('PLACES',id))
        self.layouts[id] = lay

    def storeToFile(self, filename):
        pass

    def loadFromFile(cls, filename):
        pass

    loadFromFile=classmethod(loadFromFile)