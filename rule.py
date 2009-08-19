from defines import *
class Game():
    def __init__(self,initmap):
        self.playerno = 4
        self.map = Map(len(Pos4))
#        self.getPlace() get data from player / file?
        self.PlaceAll()
        return
#        self.currentMap = initmap
#        self.player...
    def IsMovable(self,frompos,topos):
        return False
    def Battle(self,frompos,topos):
        return 0
    def PlaceAll(self):
#        self.map.Set(...)
#   place all initial data

class Player():
    def __init__(self):
        return
#get initialize position
#self.chess=...
    def IsLose(self):
        return False
    def Lost40(self,currentMap):
        return False

def canPlace(pos,playno,chess):
    if pos >= playno*30 | pos < (playno-1)*30
        return False
    pos = pos % 30
    if Pos4[pos].safe:
        return False
    if chess.prop.initrule == 0:
        return True
    elif chess.prop.initrule == 1:
        return (pos < 10)
    elif chess.prop.initrule == 2:
        return (pos < 25)
    elif chess.prop.initrule == 3:
        return ((pos == 1) | (pos == 3))
    return False #Unknown rule?
