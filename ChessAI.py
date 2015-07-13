#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
import threading
from Heuristic import Heuristic

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode, depth):
        actions = currentNode.Actions("black")
        bestMoveTuple = None

        bestMoveUtility = self.AlphaBetaSearch(currentNode=currentNode, depth=depth, actions=actions)

        #get the best move tuple
        for i in actions:
            if i.utility == bestMoveUtility:
                bestMoveTuple = i.GetMoveTuple()
                break
        return bestMoveTuple

    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, actions=None):
        if maxPlayer:
            playerColor = "black"
        else:
           playerColor = "white"

        #terminal test1
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, playerColor)
            return currentNode.utility

        if actions == None:
            if maxPlayer:
                actions = currentNode.Actions("black")
            else:
                actions = currentNode.Actions("white")

        #terminal test2
        if len(actions) == 0:
            Heuristic.ShannonHeuristic(currentNode, playerColor)
            return currentNode.utility

        if maxPlayer:
            v = -10000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 ) )
                if v >= beta:
                    return beta
                if v > alpha:
                    alpha = v
            currentNode.SetUtility(alpha)
            return alpha
        else:
            v = 10000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1 ) )
                if v <= alpha:
                    return alpha
                if v < beta:
                    beta = v
            currentNode.SetUtility(beta)
            return beta