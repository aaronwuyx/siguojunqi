#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Visible class.
"""

class Visible(object):
    """
        This class describes possible visible mode of chess.
    """
    #Nobody can see
    VIS_NONE = "VIS_NONE"
    #Everybody can see
    VIS_ALL = "VIS_ALL"
    #Only the owner can see
    VIS_SELF = "VIS_SELF"
    #Only owner's teammates (including owner himself) can see
    VIS_TEAM = "VIS_TEAM"
    
    def __getattr__(self, name):
        return valueOf(name)

    def valueOf(cls,name):
        #A list of all available values
        __enum = [Visible.VIS_NONE,
                  Visible.VIS_ALL,
                  Visible.VIS_SELF,
                  Visible.VIS_TEAM]
        if name in __enum:
            return name
        else:
            raise ValueError("Invalid value for Visible")
    valueOf = classmethod(valueOf)    
    
