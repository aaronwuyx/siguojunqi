#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the UserColor class.
"""

class UserColor(object):
    """
        This class describes possible colors of players.
        Length of this field should be 7 alphanum chars.
        Thouch currently no restriction is applied to Color names.
    """
    #black
    CLR_BLK = "CLR_BLK"
    #blue
    CLR_BLU = "CLR_BLU"
    #green
    CLR_GRN = "CLR_GRN"
    #orange
    CLR_ORG = "CLR_ORG"
    #purple
    CLR_PPL = "CLR_PPL"
    #red
    CLR_RED = "CLR_RED"
    #white
    CLR_WHT = "CLR_WHT"

    #Highlight, not for player use
    CLR_HLT = "CLR_HLT"
   
    COLORLIST = [CLR_BLK, CLR_BLU, CLR_GRN, CLR_ORG, CLR_PPL, CLR_RED, CLR_WHT]

    def __getattr__(self, name):
        return valueOf(name)
        
    def valueOf(cls, name):
        #All available values
        __enum = [UserColor.CLR_BLK, UserColor.CLR_BLU,
                  UserColor.CLR_GRN, UserColor.CLR_ORG,
                  UserColor.CLR_PPL, UserColor.CLR_RED,
                  UserColor.CLR_WHT, UserColor.CLR_HLT]
        if name in __enum:
            return name
        else:
            raise ValueError("Invalid value for UserColor")
    valueOf = classmethod(valueOf)
