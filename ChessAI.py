#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import copy

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.table = ZobristHash(size=2**24)
        self.heuristicTable = ZobristHash(size=2**24)
        self.bestMoveTuple = None
        self.bestMoveUtility = -1000

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode):
        actions = currentNode.Actions("black", self.heuristicTable)
        depth = 1
        self.bestMoveTuple = None
        self.bestMoveUtility = -1000

        try:
            def handler(signum, frame):
                print "signal received"
                raise RuntimeError
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)

            while True:
                self.bestMoveUtility = self.AlphaBetaSearch(currentNode=currentNode, depth=depth, actions=actions)

                #DEBUG
                print "search arrived at depth "+str(depth)
                depth +=1

                #get the best move tuple
                for i in actions:
                    if i.utility == self.bestMoveUtility:
                        self.bestMoveTuple = i.GetMoveTuple()
                print self.bestMoveUtility

                #new hashtables
                self.heuristicTable = copy.copy(self.table)
                self.table = ZobristHash(size=2**24)
        except RuntimeError:
            print "exception caught"
        finally:
            return self.bestMoveTuple

    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, actions=None):
        #use hashtable
        cachedValue = self.table.lookup(currentNode.board)
        if cachedValue != None:
            currentNode.SetUtility(cachedValue) #utility
            return cachedValue

        #terminal test1
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility)
            return currentNode.utility

        if actions == None:
            if maxPlayer:
                actions = currentNode.Actions("black", self.heuristicTable)
            else:
                actions = currentNode.Actions("white", self.heuristicTable)

        #terminal test2
        if len(actions) == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility)
            return currentNode.utility

        # Max
        if maxPlayer:
            v = -10000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 , None) )
                if v >= beta:
                    print('pruned in max')
                    return v
                alpha = max(alpha, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            return v

        # Min
        else:
            v = 10000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1, None ) )
                if v <= alpha:
                    print('pruned in min')
                    return v
                beta = min( beta, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            return v
