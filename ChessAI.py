#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import copy
#import time

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.table = ZobristHash(size=2**24)
        self.heuristicTable = ZobristHash(size=2**24)

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
            signal.alarm(20)
            while True:
                #htime = 0
                bestMove = self.AlphaBetaInit(currentNode=currentNode, depth=depth, depthLimit=depth)#, htime=htime)

                #DEBUG
                print "search arrived at depth "+str(depth)#+" heuristic time= "+str(htime)+"s"
                depth +=1

                #new hashtables
                #self.heuristicTable = copy.copy(self.table)
                #self.table.hashTable = {}
        except RuntimeError:
            pass
        return bestMove

    def AlphaBetaInit(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        v = -10000
        counter = 0
        inner = 1
        moves = []
        node, counter, moves, inner = currentNode.NextAction("black", counter, inner, moves)
        bestMove = None
        while node != None:
            utility = self.AlphaBetaSearch( alpha, beta, node, False, depth-1, depthLimit)
            if utility > v:
                v = utility
                bestMove = node.GetMoveTuple()
            node, counter, moves, inner = currentNode.NextAction("black", counter, inner, moves)
        self.table.insertUtility(currentNode.board, v, depthLimit)
        return bestMove

    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):#, htime=0):
        #use hashtable
        cachedValue = self.table.lookup(currentNode.board)
        if cachedValue != None and cachedValue[1] >= depth:
            return cachedValue[0]

        #start = time.time()
        #terminal test1
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility, depthLimit)
            return currentNode.utility
        #end = time.time()
        #htime += (end - start)

        # Max
        if maxPlayer:
            v = -10000
            counter = 0
            inner = 1
            moves = []
            node, counter, moves, inner = currentNode.NextAction("black", counter, inner, moves)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, False, depth-1, depthLimit)
                v = max(v, utility)#, htime) )
                if v >= beta:
                    return v
                if v > alpha:
                    alpha = v
                node, counter, moves, inner = currentNode.NextAction("black", counter, inner, moves)
            self.table.insertUtility(currentNode.board, v, depthLimit)
            return v

        # Min
        else:
            v = 10000
            counter = 0
            inner = 1
            moves = []
            node, counter, actions, inner = currentNode.NextAction("white", counter, inner, moves)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, True, depth-1, depthLimit)
                v = min(v, utility)#, htime ) )
                if v <= alpha:
                    return v
                if v < beta:
                    beta = v
                node, counter, actions, inner = currentNode.NextAction("white", counter, inner, moves)
            self.table.insertUtility(currentNode.board, v, depthLimit)
            return v
