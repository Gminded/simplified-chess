#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
from Board import *
import signal
import copy

class ChessAI:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.type = 'AI'
        self.table = ZobristHash(size=2**24)

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode):
        depth = 1
        bestMove = None
        try:
            def handler(signum, frame):
                print "signal received"
                raise RuntimeError
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(15)
            while True:
                utility = self.AlphaBetaInit(currentNode=currentNode, depth=depth, depthLimit=depth)
                print "search arrived at depth "+str(depth)+" with utility "+str(utility)
                depth +=1
        except RuntimeError:
            pass
        return bestMove

    def AlphaBetaInit(self, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        counter = 0
        inner = 1
        moves = []
        lastWasTheBest = False
        bestMove = None
        node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
        while node != None:
            utility = self.AlphaBetaSearch( currentNode=node, maxPlayer=False, depth=depth-1, depthLimit=depthLimit)
            if utility > v:
                v = utility
                bestMove = node.GetMoveTuple()
            node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
        self.table.insertUtility(currentNode.board, v, depthLimit, bestMove, True)
        return v

    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        if maxPlayer:
            color='black'
        else:
            color='white'

        #terminal test
        if depth == 0 or currentNode.board.TerminalTest(color) == currentNode.board.DEFEAT:
            Heuristic.ShannonHeuristic(currentNode, self.table, depthLimit, color)
            self.table.insertUtility(currentNode.board, currentNode.utility, depthLimit, None, maxPlayer)
            return currentNode.utility

        # If this is a terminal test don't go any deeper, because the game ended.
        
        # Max
        if maxPlayer:
            v = -1000000
            counter = 0
            inner = 1
            moves = []
            bestMove = None
            lastWasTheBest = False
            node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, False, depth-1, depthLimit)
                if v >= beta:
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = node.GetMoveTuple()
                node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
            self.table.insertUtility(currentNode.board, None, depthLimit, bestMove ,maxPlayer)
            return v

        # Min
        else:
            v = 1000000
            counter = 0
            inner = 1
            moves = []
            bestMove = None
            lastWasTheBest = False
            node, counter, actions, inner, lastWasTheBest = currentNode.NextAction("white", counter, inner, moves, self.table, lastWasTheBest)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, True, depth-1, depthLimit)
                v = min(v, utility)
                if v <= alpha:
                    bestMove = node.GetMoveTuple()
                    self.table.insertUtility(currentNode.board, v, depthLimit, bestMove ,maxPlayer)
                    return v
                if v < beta:
                    beta = v
                    bestMove = node.GetMoveTuple()
                    self.table.insertUtility(currentNode.board, v, depthLimit, bestMove ,maxPlayer)
                node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("white", counter, inner, moves, self.table, lastWasTheBest)
            return v
