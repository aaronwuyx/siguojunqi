#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the GameRecord class.
"""

from xml.sax import saxutils, make_parser
from xml.sax.handler import feature_namespaces
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

class GameRecord(object):
    """
        This class defines game records.
    """
    KW_PLY = 'players'
    KW_LAY = 'layouts'
    KW_MOV = 'moves'
    KW_EVT = 'events'
    KEYWORD = [KW_PLY, KW_LAY, KW_MOV, KW_EVT]

    #for kw in KEYWORD: kw=>self.__getattribute__[kw]
    def __init__(self, player = [], layout = [], event = [], move = []):
        if player and len(player) != PLAYERNUM:
            raise ValueError("Invalid Player list")
        if layout and len(layout) != PLAYERNUM:
            raise ValueError("Invalid Layout list")
        self.fin = False
        if player:
            self.players = list(player)
        else:
            self.players = [None]*PLAYERNUM
        if layout:
            self.layouts = list(layout)
        else:
            self.layouts = [None]*PLAYERNUM

        self.moves = list(move)
        self.events = list(event)

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
        parser = make_parser()
        parser.setFeature(feature_namespace, 0)
        dh = recordParserSAX()
        parser.setHandler(dh)
        parser.parse(filename)
    loadFromFile=classmethod(loadFromFile)

    class recordParserSAX(saxutils.XMLFilterBase):
        def __init__(self):
            (self.inMove, self.inEvent, self.inLayout, self.inPlayer) = (False, False, False, False)
            self.playerid = -1
            self.layoutid = -1
            self.pl = [None]*PLAYERNUM
            self.la = [None]*PLAYERNUM
            self.mv = []
            self.ev = []

        def startElement(self, name, attrs):
            """
                First version of parser, assume everything is OK.
            """
            if name == GameRecord.KW_PLY:
                self.playerid = attrs.get('id', None)
                from Rule import isValidPlayer
                if isValidPlayer(self.playerid):
                    self.inPlayer = True
                    self.playerch = ''
            elif name == GameRecord.KW_LAY:
                self.layoutid = attrs.get('id', None)
                from Rule import isValidPlayer
                if isValidPlayer(self.layoutid):
                    self.inLayout = True
                    self.layoutch = ''
            elif name == GameRecord.KW_MOV:
                self.inMove = True
                self.movech = ''
            elif name == GameRecord.KW_EVT:
                self.inEvent = True
                self.eventch = ''

        def characters(self, ch):
            if self.inPlayer:
                self.playerch = self.playerch + ch
            if self.inLayout:
                self.layoutch = self.layoutch + ch
            if self.inMove:
                self.movech = self.movech + ch
            if self.inEvent:
                self.eventch = self.eventch + ch

        def endElement(self, name):
            if name == GameRecord.KW_PLY:
                from Rule import isValidPlayer
                if self.inPlayer and isValidPlayer(self.playerid):
                    from Player import Player
                    self.pl[self.playerid] = Player.fromStringID(self.playerch, self.playerid)
                self.playerid = -1
                self.inPlayer = False
            elif name == GameRecord.KW_LAY:
                from Rule import isValidPlayer
                if self.inLayout and isValidPlayer(self.layoutid):
                    from Layout import Layout
                    self.la[self.layoutid] = Layout.fromString(self.layoutch, self.layoutid)
                self.layoutid = -1
                self.inLayout = False
            elif name == GameRecord.KW_MOV:
                from Movement import Movement
                self.mv.append(Movement.fromString(self.movech))
                self.inMove = False
            elif name == GameRecord.KW_EVT:
                self.ev.append(RecordEvent.fromString(self.eventch))
                self.inEvent = False

        def error(self, exception):
            print('Exception occurred during parsing XML')

if __name__=='__main__':
    a = GameRecord()