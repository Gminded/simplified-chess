#! /usr/bin/env python2.7

from Heuristic import Heuristic
from ZobristHash import ZobristHash
import signal
import copy
from ChessNode import ChessNode

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

    def GetMove(self, board, timeout):
        depth = 1
        bestMove = None
        boardBackup = copy.deepcopy(board)
        self.statesVisited = 1
        try:
            def handler(signum, frame):
                print "timeout triggered"
                raise KeyboardInterrupt
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            while True:
                utility, bestMove = self.AlphaBetaInit(depth=depth, board=board)
                depth +=1

                # It's pointless to go on if we know we are going to win or lose
                if 500000000 <= utility or utility <= -500000000:
                    signal.alarm(0)
                    break

        except KeyboardInterrupt:
            pass
        print "search arrived at depth "+str(depth)+" with utility "+str(utility)
        print('states visited: '+str(self.statesVisited))
        print('hash table hits: '+str(self.table.hits))
        print('hash table size: '+str(len(self.table.hashTable)))
        return bestMove, boardBackup

    def AlphaBetaInit(self, depth=0, board=None):
        v = -20000000
        maxUtility = v
        myPreviousMove = board.previousMove
        currentNode = ChessNode(myPreviousMove)
        bestMove = move = currentNode.NextAction("b", self.table, board)
        while move != None:
            board.movePiece(move)
            node = ChessNode(move)
            # Use transposition table not to search already visisted states
            entry = self.table.lookup(board)
            if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
                v = max(v, entry[self.table.SCORE])
            else:
                v = max( v, self.AlphaBetaSearch(currentNode=node, maxPlayer=False, depth=depth-1, board=board) )
                #Store exact utility value in table
                self.table.insert(board, v, depth, None , None)
            #Restore previous state before continuing
            board.undoMove(move,myPreviousMove)
            if v > maxUtility:
                maxUtility = v
                bestMove = move
            move = currentNode.NextAction("b", self.table, board)
        self.table.insert(board, v,depth, bestMove, None)
        return maxUtility, bestMove.moveTuple

    def AlphaBetaSearch(self, alpha=-20000000, beta=20000000,
                        currentNode=None, maxPlayer=True, depth=0, board=None):
        self.statesVisited+=1

        if maxPlayer:
            color='b'
        else:
            color='w'

        # If this is a terminal state don't go any deeper, because the game ended.
        if board.terminalTest(color) == board.DEFEAT:
            utility = Heuristic.ShannonHeuristic(currentNode, self.table, board)
            if maxPlayer: #we are losing so the value is negative
                utility -=self.DEFEATWEIGHT
            else: #minPlayer: we are winning so the value is positive
                utility +=self.DEFEATWEIGHT
            return utility

        # Cut off
        if depth == 0:
            utility = Heuristic.ShannonHeuristic(currentNode, self.table, board)
            return utility

        
        # Max
        if maxPlayer:
            v = -20000000
            bestMove = None
            myPreviousMove = board.previousMove
            move = currentNode.NextAction("b", self.table, board)
            while move != None:
                board.movePiece(move)
                node = ChessNode( move )
                # Use transposition table not to search already visisted states
                entry = self.table.lookup(board)
                if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
                    v = max(v, entry[self.table.SCORE])
                else:
                    v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1,  board))
                    #Store exact utility value in table
                    self.table.insert(board, v, depth, None , None)
                #Restore previous state before continuing
                board.undoMove(node.getMove(),myPreviousMove)
                if v >= beta:
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = move
                move = currentNode.NextAction("b", self.table, board)
            self.table.insert(board, v, depth, bestMove , None)
            return v

        # Min
        else:
            v = 20000000
            bestMove = None
            myPreviousMove = board.previousMove
            move = currentNode.NextAction("w", self.table, board)
            while move != None:
                board.movePiece(move)
                node = ChessNode(move)
                # Use transposition table not to search already visisted states
                entry = self.table.lookup(board)
                if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
                    v = min(v, entry[self.table.SCORE])
                else:
                    v = min(v, self.AlphaBetaSearch(alpha, beta, node, True, depth-1, board))
                    #Store exact utility value in table
                    self.table.insert(board, v, depth, None , None)
                #Restore previous state before continuing
                board.undoMove(node.getMove(),myPreviousMove)
                if v <= alpha:
                    return v
                if v < beta:
                    beta = v
                    bestMove = move
                move = currentNode.NextAction("w", self.table, board)
            self.table.insert(board, v, depth, None , bestMove)
            return v
