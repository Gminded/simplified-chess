#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import copy

class ChessAI:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.type = 'AI'
        self.table = ZobristHash(size=2**24)
        self.DEFEATWEIGHT=1000000000

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode, board):
        depth = 1
        bestMove = None
        boardBackup = copy.deepcopy(board)
        try:
            def handler(signum, frame):
                print "signal received"
                raise RuntimeError
            signal.signal(signal.SIGALRM, handler)
            #signal.alarm(10)
            while depth<=3:
                utility, bestMove = self.AlphaBetaInit(currentNode=currentNode, depth=depth,t board=board)
                print "search arrived at depth "+str(depth)+" with utility "+str(utility)
                depth +=1

                # It's pointless to go on if we know are going to win or lose
                if 500000000 <= utility or utility <= -500000000:
                    print('Stopping early because of terminal state.')
                    signal.alarm(0)
                    break

        except RuntimeError:
            pass
        board = boardBackup
        return bestMove

    def AlphaBetaInit(self, currentNode=None, depth=0, board=None):
        v = -20000000
        maxUtility = v
        myPreviousMove = board.previousMove
        node = currentNode.NextAction("b", self.table, board)
        bestMove = node.getMove()
        while node != None:
            v = max( v, self.AlphaBetaSearch(myPreviousMove, currentNode=node, maxPlayer=False, depth=depth-1, board=board) )
            #Restore previous state before continuing
            board.undoMove(node.getMove(),myPreviousMove)
            if v > maxUtility:
                maxUtility = v
                bestMove = node.getMove()
            node = currentNode.NextAction("b", self.table, board)
        self.table.insert(board, v, depth, bestMove, True)
        return maxUtility, bestMove.moveTuple

    def AlphaBetaSearch(self, previousMove, alpha=-20000000, beta=20000000,\
                        currentNode=None, maxPlayer=True, depth=0, board=None):
        if maxPlayer:
            color='b'
        else:
            color='w'

        # If this is a terminal state don't go any deeper, because the game ended.
        if board.terminalTest(color) == board.DEFEAT:
            utility = Heuristic.ShannonHeuristic(currentNode, self.table, depth, color, board)
            if maxPlayer: #we are losing so the value is negative
                utility -=self.DEFEATWEIGHT
            else: #minPlayer: we are winning so the value is positive
                utility +=self.DEFEATWEIGHT
            self.table.insert(board, utility, depth, None, None)
            return utility

        # Cut off
        if depth == 0:
            utility = Heuristic.ShannonHeuristic(currentNode, self.table, color, board)
            self.table.insert(board, utility, depth, None, None)
            return utility

        
        # Max
        if maxPlayer:
            v = -20000000
            bestMove = None
            myPreviousMove = board.previousMove
            node = currentNode.NextAction("b", self.table, board)
            while node != None:
                v = max(v, self.AlphaBetaSearch( myPreviousMove, alpha, beta, node, False, depth-1, board))
                #Restore previous state before continuing
                board.undoMove(node.getMove(),previousMove)
                if v >= beta:
                    self.table.insert(board, None, depth, node.getMove() , None)
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = node.getMove()
                node = currentNode.NextAction("b", self.table, board)
            self.table.insert(board, None, depth, bestMove , None)
            return v

        # Min
        else:
            v = 20000000
            bestMove = None
            myPreviousMove = board.previousMove
            node = currentNode.NextAction("w", self.table, board)
            while node != None:
                v = min(v, self.AlphaBetaSearch(myPreviousMove, alpha, beta, node, True, depth-1, board))
                #Restore previous state before continuing
                board.undoMove(node.getMove(),previousMove)
                if v <= alpha:
                    self.table.insert(board, None, depth, node.getMove() , None)
                    return v
                if v < beta:
                    beta = v
                    bestMove = node.getMove()
                node = currentNode.NextAction("w", self.table, board)
            self.table.insert(board, None, depth, None , bestMove)
            return v
