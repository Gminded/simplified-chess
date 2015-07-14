#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import os

continueIterative = True

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
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
        actions = currentNode.Actions("black", self.table)

        worker_proc = os.fork()

        if worker_proc == 0:
            self.GetIterativeMove(currentNode, actions)
        else:

            def handler(signum, frame):
                print "signal received"
                continueIterative = False
                os.kill(worker_proc, signal.SIGKILL)

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(5)
            try:
                os.wait()
            except OSError:
                pass

        bestMoveDepth = -1
        #get the best move tuple
        for i in actions:
            if i.bestMoveDepth > bestMoveDepth:
                bestMoveDepth = i.bestMoveDepth
                bestMoveTuple = i.GetMoveTuple()
        return bestMoveTuple

    def GetIterativeMove(self, currentNode, actions):
        bestMoveTuple = None
        depth = 1
        continueIterative = True
        while continueIterative:
            self.AlphaBetaSearch(currentNode=currentNode, depth=depth, actions=actions, initialDepth=depth)
            depth +=1
            #DEBUG
            print "search arrived at depth "+str(depth)



    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, actions=None, initialDepth=0):
        #use hashtable
        if currentNode.bestMoveDepth > initialDepth:
            cachedValue = self.table.lookup(currentNode.board)
            if cachedValue != None:
                currentNode.SetUtility(cachedValue) #utility
                currentNode.bestMoveDepth = initialDepth
                return cachedValue

        #terminal test1
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility)
            currentNode.bestMoveDepth = initialDepth
            return currentNode.utility

        if actions == None:
            if maxPlayer:
                actions = currentNode.Actions("black", self.table)
            else:
                actions = currentNode.Actions("white", self.table)

        #terminal test2
        if len(actions) == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility)
            currentNode.bestMoveDepth = initialDepth
            return currentNode.utility

        # Max
        if maxPlayer:
            v = -10000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 , None, initialDepth) )
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            currentNode.bestMoveDepth = initialDepth
            return v

        # Min
        else:
            v = 10000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1, None, initialDepth ) )
                if v <= alpha:
                    return v
                beta = max( beta, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            currentNode.bestMoveDepth = initialDepth
            return v
