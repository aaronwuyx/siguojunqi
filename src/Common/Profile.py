#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This file defines the Profile class.
"""

import os

class Profile( object ):
    """
        This class describes user profile, you can use it to create a Player class.
    """
    VER = 1 # Identify different profiles

    def __init__( self, name ):
        self.name = name
        self.ver = Profile.VER
        self.layoutfile = None
        self.backgroundfile = None
        self.profile = None

    def getBackgroundFile( self ):
        return self.backgroundfile

    def setBackgroundFile( self , filename ):
        self.backgroundfile = filename
        if filename and not os.path.exists( os.path.abspath( filename ) ):
            print( 'warning : file "%s" does not exist.' %(filename))

    def getLayoutFile( self ):
        return self.layoutfile

    def setLayoutFile( self, filename ):
        self.layoutfile = filename
        if filename and not os.path.exists( os.path.abspath( filename ) ):
            print( 'warning : file "%s" does not exist.' %(filename))

    def load( cls, filename):
        text = open( filename, 'r' ).readlines()
        if len(text) < 1:
            print("Invalid file syntax")
            return
        if not text[0].startswith("VER "+str(Profile.VER)):
            print("Invalid file syntax, or incorrect profile version, try\
            convertion first.")
            return
        name = None
        bg = None
        lay = None
        for line in text[1:]:
            if line.startswith( 'Name=' ):
                name = line[5:].strip()
            elif line.startswith( 'BackgroundFile='):
                bg = line[15:].strip()
            elif line.startswith( 'LayoutFile='):
                lay = line[11:].strip()
        if not name:
            print("Invalid profile, should at least specify user name")
            return
        p = Profile(name)
        if bg:
            p.setBackgroundFile(bg)
        if lay:
            p.setLayoutFile(lay)
        return p
    load = classmethod(load)

    def save( self, filename ):
        f = open( filename, 'w')
        f.write('VER %s\n'%(Profile.VER))
        f.write('\n')
        f.write('Name=%s\n' % ( self.name ) )
        if self.backgroundfile:
            f.write('BackgroundFile=%s\n' % ( self.backgroundfile ) )
        if self.layoutfile:
            f.write('Layoutfile=%s\n' % ( self.layoutfile ) )
        f.close()

    def __str__( self ):
        return 'name = %s, layfile = %s, bgfile = %s' % ( self.name,
                                                          self.layoutfile,
                                                          self.backgroundfile )

if __name__ == '__main__':
    p = Profile( 'test' )
    print( p )
    p.save('test')
    q = Profile.load('test')
    print( q )
