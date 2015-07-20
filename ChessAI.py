#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
from ChessBoard import *
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
        self.DEFEATWEIGHT=1000000000
        self.prunedAlphaBeta=0

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode):
        depth = 1
        bestMove = None
        self.prunedAlphaBeta=0
        try:
            def handler(signum, frame):
                print "signal received"
                raise RuntimeError
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(15)
            while True:
                #htime = 0
                bestMove, utility = self.AlphaBetaInit(currentNode=currentNode, depth=depth, depthLimit=depth)#, htime=htime)

                #DEBUG
                print "search arrived at depth "+str(depth)#+" heuristic time= "+str(htime)+"s"
                depth +=1

                # It's pointless to go on if we know are going to win or lose
                if 500000000 <= utility or utility <= -500000000:
                    print('Stopping early because of terminal state.')
                    signal.alarm(0) #disable alarm because we're done
                    break

        except RuntimeError:
            pass
        print('Number of branches pruned due to alpha-beta: '+str(self.prunedAlphaBeta))
        return bestMove

    def AlphaBetaInit(self, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        counter = 0
        inner = 1
        moves = []
        lastWasTheBest = False
        node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
        bestMove = None
        # Initialize v before cycling through the other actions
        if node != None:
            v = self.AlphaBetaSearch( currentNode=node, maxPlayer=False, depth=depth-1, depthLimit=depthLimit)
            bestMove = node.GetMoveTuple()
            node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
        while node != None:
            utility = self.AlphaBetaSearch( currentNode=node, maxPlayer=False, depth=depth-1, depthLimit=depthLimit)
            if utility > v:
                v = utility
                bestMove = node.GetMoveTuple()
            node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
        self.table.insertUtility(currentNode.board, v, depthLimit, bestMove, True)
        print "best utility "+str(v)
        return bestMove, v

    def AlphaBetaSearch(self, alpha=-10000, beta=10000, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):#, htime=0):
        #use hashtable
        #cachedValue = self.table.lookup(currentNode.board)
        #if cachedValue != None and cachedValue[1] >= depth:
        #    return cachedValue[0]

        if maxPlayer:
            color='b'
        else:
            color='w'

        # If this is a terminal test don't go any deeper, because the game ended.
        if currentNode.board.TerminalTest(color) == DEFEAT:
            Heuristic.ShannonHeuristic(currentNode, self.table, depthLimit, color)
            if maxPlayer: #we are losing so the value is negative
                currentNode.utility-=self.DEFEATWEIGHT
            else: #minPlayer: we are losing so the value is positive
                currentNode.utility+=self.DEFEATWEIGHT

        #Cut off
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table, depthLimit, color)
            self.table.insertUtility(currentNode.board, currentNode.utility, depthLimit, None, maxPlayer)
            return currentNode.utility
        #end = time.time()
        #htime += (end - start)


        
        # Max
        if maxPlayer:
            v = -2000000000
            counter = 0
            inner = 1
            moves = []
            bestMove = None
            lastWasTheBest = False
            node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, False, depth-1, depthLimit)
                v = max(v, utility)#, htime) )
                if v >= beta:
                    bestMove = node.GetMoveTuple()
                    self.table.insertUtility(currentNode.board, v, depthLimit, bestMove ,maxPlayer)
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = node.GetMoveTuple()
                    self.table.insertUtility(currentNode.board, v, depthLimit, bestMove ,maxPlayer)
                node, counter, moves, inner, lastWasTheBest = currentNode.NextAction("black", counter, inner, moves, self.table, lastWasTheBest)
            return v

        # Min
        else:
            v = 2000000000
            counter = 0
            inner = 1
            moves = []
            bestMove = None
            lastWasTheBest = False
            node, counter, actions, inner, lastWasTheBest = currentNode.NextAction("white", counter, inner, moves, self.table, lastWasTheBest)
            while node != None:
                utility = self.AlphaBetaSearch( alpha, beta, node, True, depth-1, depthLimit)
                v = min(v, utility)#, htime ) )
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
