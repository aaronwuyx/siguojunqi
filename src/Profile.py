#CLI_SIDE, not common

import os
from Player import Player
from Layout import Layout
from Layout import load

PROFILEVER = 1 # Identify different profiles

class Profile( Player ):
    def __init__( self, name ):
        Player.__init__( self, name )
        self.__filename = self.__name + '.cfg'
        self.__bgfile = 'blank.gif'
        self.__layfile = self.__name + '.layout'
        self.__ver = PROFILEVER

        try:
            self.load()
        except IOError:
            pass
        #logging.info( self.__str__() )

    def getBgFile( self ):
        return self.__bgfile

    def setBgFile( self , filename ):
        if os.path.exists( os.path.abspath( filename ) ):
            self.__bgfile = os.path.abspath( filename )

    def setLayoutFile( self, filename ):
        if os.path.exists( os.path.abspath( filename ) ):
            self.__layfile = os.path.abspath( filename )
        else:
            self.__layfile = os.path.abspath( self.__name + '.layout' )

    def getLayoutFile( self ):
        return self.__layfile

    def getTotal( self ):
        return self.__win + self.__lose + self.__draw

    def getWinPercent( self ):
        if self.getTotal() == 0:
            return 0.0
        else:
            return float( self.getWin() ) / self.getTotal()

    def load( self ):
        f = open( self.__filename, 'r' )
        text = f.readlines()
        f.close()
        for line in text:
            if line.startswith( 'name=' ):
                if self.__name != line[5:].strip():
                    return
            elif line.startswith( 'ver=' ):
                try:
                    ver = int( line[5:].strip() )
                except:
                    pass
                if ver > PROFILEVER:
                    return
            elif line.startswith( 'bgfile=' ):
                self.__bgfile = line[7:].strip()
            elif line.startswith( 'layfile=' ):
                self.__layfile = line[8:].strip()

    def save( self ):
        f = open( self.filename, 'w' )
        f.write( 'name=%s\n' % ( self.__name ) )
        f.write( 'ver=%d\n' % ( self.__ver ) )
        f.write( 'bgfile=%s\n' % ( self.__bgfile ) )
        f.write( 'layfile=%s\n' % ( self.__layfile ) )
        f.close()

    def saveLayout( self, layout ):
        layout.save( self.__layfile )

    def loadLayout( self ):
        l = Layout( self.__id )
        l.setToDefault()
        if not os.path.exists( self.__layfile ):
            return l
        try:
            m = load( self.__layfile, self.__id )
            return m
        except ValueError:
            return l

    def __str__( self ):
        return 'ver=%d, name=%s, id=%d, color=%s' % ( self.__ver, self.__name, self.__id, self.getActiveBgcolor() )

if __name__ == '__main__':
    p = Profile( 'test' )
    print( p )
    p.save()
    p.load()
    print( p )
