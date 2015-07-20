#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal

class ChessAI:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.type = 'AI'
        self.table = ZobristHash(size=2**24)
        self.DEFEATWEIGHT=1000000000
        self.prunedAlphaBeta=0 #count of branches pruned due to alpha-beta

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
            signal.alarm(1500)
            while True:
                utility, bestMove = self.AlphaBetaInit(currentNode=currentNode, depth=depth, depthLimit=depth)
                print "search arrived at depth "+str(depth)+" with utility "+str(utility)
                depth +=1

                # It's pointless to go on if we know are going to win or lose
                if 500000000 <= utility or utility <= -500000000:
                    print('Stopping early because of terminal state.')
                    signal.alarm(0)
                    break

        except RuntimeError:
            pass
        print('Number of branches pruned due to alpha-beta: '+str(self.prunedAlphaBeta))
        return bestMove

    def AlphaBetaInit(self, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        v = -20000000
        bestMove = None
        maxUtility = v
        node = currentNode.NextAction("b", self.table)
        while node != None:
            v = max( v, self.AlphaBetaSearch( currentNode=node, maxPlayer=False, depth=depth-1, depthLimit=depthLimit) )
            if v > maxUtility:
                maxUtility = v
                bestMove = node.getMove()
            node = currentNode.NextAction("b", self.table)
        self.table.insertUtility(currentNode.board, v, depthLimit, bestMove, True)
        return maxUtility, bestMove.moveTuple

    def AlphaBetaSearch(self, alpha=-20000000, beta=20000000, currentNode=None, maxPlayer=True, depth=0, depthLimit=0):
        if maxPlayer:
            color='b'
        else:
            color='w'

        # If this is a terminal state don't go any deeper, because the game ended.
        if currentNode.board.terminalTest(color) == currentNode.board.DEFEAT:
            Heuristic.ShannonHeuristic(currentNode, self.table, depthLimit, color)
            if maxPlayer: #we are losing so the value is negative
                currentNode.utility-=self.DEFEATWEIGHT
            else: #minPlayer: we are losing so the value is positive
                currentNode.utility+=self.DEFEATWEIGHT
            self.table.insertUtility(currentNode.board, currentNode.utility, depthLimit, None, None)
            return currentNode.utility

        # Cut off
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, self.table, depthLimit, color)
            self.table.insertUtility(currentNode.board, currentNode.utility, depthLimit, None, None)
            return currentNode.utility

        
        # Max
        if maxPlayer:
            v = -20000000
            bestMove = None
            node = currentNode.NextAction("b", self.table)
            while node != None:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1, depthLimit) )
                if v >= beta:
                    self.prunedAlphaBeta+=1
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = node.getMove()
                node = currentNode.NextAction("b", self.table)
            self.table.insertUtility(currentNode.board, None, depthLimit, bestMove , None)
            return v

        # Min
        else:
            v = 20000000
            bestMove = None
            node = currentNode.NextAction("w", self.table)
            while node != None:
                v = min( v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1, depthLimit)  )
                if v <= alpha:
                    self.prunedAlphaBeta+=1
                    return v
                if v < beta:
                    beta = v
                    bestMove = node.getMove()
                node = currentNode.NextAction("w", self.table)
            self.table.insertUtility(currentNode.board, v, depthLimit, None , bestMove)
            return v
