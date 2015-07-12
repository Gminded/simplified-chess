#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from ChessRules import ChessRules
from Heuristic import Heuristic

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

    def GetMove(self, currentNode):
        actions = currentNode.Actions("black")
        bestMoveUtility = self.AlphaBetaSearch(currentNode=currentNode, depth=4)
        bestMoveTuple = None

        #get the best move tuple
        for i in actions:
            if i.utility == bestMoveUtility:
                bestMoveTuple = i.GetMoveTuple()
                break
        return bestMoveTuple


    def AlphaBetaSearch(self, alpha=-1000, beta=1000, currentNode=None, maxPlayer=True, depth=0):
        if maxPlayer:
            actions = currentNode.Actions("black")
        else:
            actions = currentNode.Actions("white")

        #terminal test
        if depth == 0 or len(actions) == 0:
            Heuristic.HeuristicFunction(currentNode)
            return currentNode.utility

        if maxPlayer:
            v = -1000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 ) )
                if v >= beta:
                    return beta
                if v > alpha:
                    alpha = v
            return alpha
        else:
            v = 1000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1 ) )
                if v <= alpha:
                    return alpha
                if v < beta:
                    beta = v
            return beta