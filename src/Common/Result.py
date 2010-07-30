#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This file defines the Result class.
"""

class Result(object):
    """
        This class describes possible Result of a battle,
        all elements in Result is 7 alphanum chars.
    """
    #No result, default value in some cases.
    RES_NON = "RES_NON"
    #the chess which moves win.
    RES_WIN = "RES_WIN"
    #the chess which moves lose.
    RES_LOS = "RES_LOS"
    #neither wins.
    RES_EQU = "RES_EQU"
    
    def __getattr__(self, name):
        return valueOf(name)
        
    def valueOf(cls, name):
        #All available values
        __enum = [Result.RES_NON,
                  Result.RES_WIN,
                  Result.RES_LOS,
                  Result.RES_EQU]
        if name in __enum:
            return name
        else:
            raise ValueError("Invalid value for Result")

    valueOf = classmethod(valueOf)
