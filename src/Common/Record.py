#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the GameRecord class.
"""

from xml.sax import saxutils, make_parser
from xml.sax.handler import feature_namespaces
from xml.dom import minidom
from xml.dom.minidom import Node

from Rule import PLAYERNUM, isValidPlayer

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
        return self.toString()

    def toString(self):
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
    KW_PLY = 'player'
    KW_LAY = 'layout'
    KW_MOV = 'move'
    KW_EVT = 'event'
    XML_RCD = 'records'
    XML_PLY = 'players'
    XML_LAY = 'layouts'
    XML_MOV = 'movements'
    XML_EVT = 'events'
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

    #def fillLayout(self, la):
    #    if isinstance(la, list) and len(la) == PLAYERNUM:
    #        self.layouts = la
    #        return True
    #    return False

    def startRecord(self, players):
        if len(self.events) > 0:
            print('Warning: INIT event is not the first event')
        self.events.append(RecordEvent('INIT'))
        self._fillPlayer(players)

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
        if not isValidPlayer(id):
            raise ValueError("Invalid player id: %d"%(id))
        self.events.append(RecordEvent('EXIT',id))

    def recordLayout(self, id, lay):
        if not isValidPlayer(id):
            raise ValueError("Invalid player id: %d"%(id))
        if self.layouts[id]:
            print("Warning: Layout data already exist, overlay it")
        self.events.append(RecordEvent('PLACE',id))
        self.layouts[id] = lay

    def storeToFile(self, filename):
        doc = minidom.Document()
        root = doc.createElement(GameRecord.XML_RCD)
        doc.appendChild(root)
        plys = doc.createElement(GameRecord.XML_PLY)
        lays = doc.createElement(GameRecord.XML_LAY)
        movs = doc.createElement(GameRecord.XML_MOV)
        evts = doc.createElement(GameRecord.XML_EVT)
        root.appendChild(plys)
        root.appendChild(lays)
        root.appendChild(movs)
        root.appendChild(evts)
        for i in range(PLAYERNUM):
            if self.players[i]:
                ply = doc.createElement(GameRecord.KW_PLY)
                ply.setAttribute('id',str(i))
                plys.appendChild(ply)
                ptext = doc.createTextNode(self.players[i].toString())
                ply.appendChild(ptext)
            if self.layouts[i]:
                lay = doc.createElement(GameRecord.KW_LAY)
                lay.setAttribute('id',str(i))
                lays.appendChild(lay)
                ltext = doc.createTextNode(self.layouts[i].toString())
                lay.appendChild(ltext)
        for item in self.moves:
            mov = doc.createElement(GameRecord.KW_MOV)
            movs.appendChild(mov)
            mtext = doc.createTextNode(item.toString())
            mov.appendChild(mtext)
        for item in self.events:
            evt = doc.createElement(GameRecord.KW_EVT)
            evts.appendChild(evt)
            etext = doc.createTextNode(item.toString())
            evt.appendChild(etext)
        output = open(filename, 'w')
        s = doc.toprettyxml(indent="    ")
        print s
        output.write(s)
        output.close()

    def loadFromFileDOM(cls, filename):
        doc = minidom.parse(filename)
        #print doc.toprettyxml(indent="    ")
        rec = GameRecord()
        for node1 in doc.getElementsByTagName(GameRecord.XML_RCD):
            for node2 in node1.getElementsByTagName(GameRecord.XML_PLY):
                for node3 in node2.getElementsByTagName(GameRecord.KW_PLY):
                    idStr = node3.getAttribute('id')
                    playerStr = ''
                    for node4 in node3.childNodes:
                        if node4.nodeType == Node.TEXT_NODE:
                            playerStr += node4.data
                    try:
                        id = int(idStr.strip())
                        print(type(id))
                        if isValidPlayer(id):
                            from Player import Player
                            rec.players[id] = Player.fromStringID(playerStr.strip(), id)
                    except ValueError:
                        break
            for node2 in node1.getElementsByTagName(GameRecord.XML_LAY):
                for node3 in node2.getElementsByTagName(GameRecord.KW_LAY):
                    idStr = node3.getAttribute('id')
                    layoutStr = ''
                    for node4 in node3.childNodes:
                        if node4.nodeType == Node.TEXT_NODE:
                            layoutStr += node4.data
                    try:
                        id = int(idStr.strip())
                        if isValidPlayer(id):
                            from Layout import Layout
                            rec.layouts[id] = Layout.fromString(layoutStr, id)
                    except ValueError:
                        print('Warning: Invalid id number , ignore it')
                        break
            for node2 in node1.getElementsByTagName(GameRecord.XML_MOV):
                for node3 in node2.getElementsByTagName(GameRecord.KW_MOV):
                    moveStr = ''
                    for node4 in node3.childNodes:
                        if node4.nodeType == Node.TEXT_NODE:
                            moveStr += node4.data
                    from Movement import Movement
                    rec.moves.append(Movement.fromString(moveStr))
            for node2 in node1.getElementsByTagName(GameRecord.XML_EVT):
                for node3 in node2.getElementsByTagName(GameRecord.KW_EVT):
                    eventStr = ''
                    for node4 in node3.childNodes:
                        if node4.nodeType == Node.TEXT_NODE:
                            eventStr += node4.data
                    rec.events.append(RecordEvent.fromString(eventStr))
        return rec

    def loadFromFileSAX(cls, filename):
        parser = make_parser()
        parser.setFeature(feature_namespace, 0)
        dh = recordParserSAX()
        parser.setHandler(dh)
        parser.parse(filename)
    loadFromFile=classmethod(loadFromFileDOM)

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
                    self.players[self.playerid] = Player.fromStringID(self.playerch, self.playerid)
                self.playerid = -1
                self.inPlayer = False
            elif name == GameRecord.KW_LAY:
                from Rule import isValidPlayer
                if self.inLayout and isValidPlayer(self.layoutid):
                    from Layout import Layout
                    self.layouts[self.layoutid] = Layout.fromString(self.layoutch, self.layoutid)
                self.layoutid = -1
                self.inLayout = False
            elif name == GameRecord.KW_MOV:
                from Movement import Movement
                self.moves.append(Movement.fromString(self.movech))
                self.inMove = False
            elif name == GameRecord.KW_EVT:
                self.events.append(RecordEvent.fromString(self.eventch))
                self.inEvent = False

        def error(self, exception):
            print('Error occurred during parsing XML')

if __name__=='__main__':
    testSave = False
    if testSave:
        from Player import Player
        from UserColor import UserColor
        from Layout import Layout
        from Movement import Movement
        #Suppose PLAYERNUM == 4
        p = [Player('a'), Player('b'), Player('c'), Player('d')]
        p[0].setColor(UserColor.CLR_RED)
        p[1].setColor(UserColor.CLR_BLU)
        p[2].setColor(UserColor.CLR_BLK)
        p[3].setColor(UserColor.CLR_GRN)
        q = [Layout(i) for i in range(PLAYERNUM)]
        for item in q:
            item.setToDefault()
        m = [Movement.fromString('0,3,5,0,RES_WIN'),Movement.fromString('1,3,5,0,RES_LOS')]

        grec = GameRecord()
        grec.startRecord(p)
        for i in range(PLAYERNUM):
            grec.recordLayout(i, q[i])
        for item in m:
            grec.recordMove(item)
        for i in range(PLAYERNUM):
            grec.recordExit(i)
        grec.stopRecord()
        grec.storeToFile("test1.xml")

    krec = GameRecord.loadFromFile('test1.xml')
    from pprint import pprint
    pprint(krec.players)
    pprint(krec.layouts)
    pprint(krec.moves)
    pprint(krec.events)
