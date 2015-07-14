#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import thread
import threading

continueIterative = True
bestMoveUtility = -1
worker_thread = None
semaphore = None

def handler(signum, frame):
    continueIterative = False
    worker_thread.exit()
    semaphore.release()


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

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)
        semaphore = threading.Semaphore(0)
        worker_thread = thread.start_new_thread(self.GetIterativeMove, (currentNode, actions) )
        semaphore.acquire()
        #get the best move tuple
        for i in actions:
            if i.utility == bestMoveUtility:
                bestMoveTuple = i.GetMoveTuple()
                break
        return bestMoveTuple

    def GetIterativeMove(self, currentNode, actions):
        bestMoveTuple = None
        depth = 1
        continueIterative = True
        while continueIterative:
            bestMoveUtility = self.AlphaBetaSearch(currentNode=currentNode, depth=depth, actions=actions)
            depth +=1
            #DEBUG
            print "search arrived at depth "+str(depth)+" with utility "+str(bestMoveUtility)



    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, actions=None):
        #use hashtable
        if depth == 0:
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
                actions = currentNode.Actions("black", self.table)
            else:
                actions = currentNode.Actions("white", self.table)

        #terminal test2
        if len(actions) == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table)
            self.table.insertUtility(currentNode.board, currentNode.utility)
            return currentNode.utility

        # Max
        if maxPlayer:
            v = -10000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 ) )
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            return v

        # Min
        else:
            v = 10000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1 ) )
                if v <= alpha:
                    return v
                beta = max( beta, v)
            self.table.insertUtility(currentNode.board, v)
            currentNode.SetUtility(v)
            return v
