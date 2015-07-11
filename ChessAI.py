#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from ChessRules import ChessRules

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.Rules = ChessRules()

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode, currentColor):
        pass

    def AlphaBetaSearch(self, Alpha=-1000, Beta=1000, currentNode=None, MaxPlayer=True, depth=0, limit=2):
        pass