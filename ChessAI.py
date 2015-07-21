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

    def GetMove(self, board):
        depth = 1
        bestMove = None
        boardBackup = copy.deepcopy(board)
        self.statesVisited = 1
        try:
            def handler(signum, frame):
                print "signal received"
                raise KeyboardInterrupt
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(12)
            while True:
                utility, bestMove = self.AlphaBetaInit(depth=depth, board=board)
                print "search arrived at depth "+str(depth)+" with utility "+str(utility)
                depth +=1

                # It's pointless to go on if we know we are going to win or lose
                if 500000000 <= utility or utility <= -500000000:
                    print('Stopping early because of terminal state.')
                    signal.alarm(0)
                    break

        except KeyboardInterrupt:
            pass
        print('states visited: '+str(self.statesVisited))
        print('hash table hits: '+str(self.table.hits))
        print('hash table size: '+str(len(self.table.hashTable)))
        return bestMove, boardBackup

    def AlphaBetaInit(self, depth=0, board=None):
        v = -20000000
        maxUtility = v
        myPreviousMove = board.previousMove
        currentNode = ChessNode(myPreviousMove)
        bestMove = move = currentNode.NextAction("b", self.table, board, depth)
        while move != None:
            board.movePiece(move)
            node = ChessNode(move)
            # Use transposition table not to search already visisted states
            entry = self.table.lookup(board)
            #if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
            #    v = max(v, entry[self.table.SCORE])
            #else:
            v = max( v, self.AlphaBetaSearch(myPreviousMove, currentNode=node, maxPlayer=False, depth=depth-1, depthLimit=depth, board=board) )
                #Store exact utility value in table
                #self.table.insert(board, v, 0, None , None)
            #Restore previous state before continuing
            board.undoMove(move,myPreviousMove)
            if v > maxUtility:
                maxUtility = v
                bestMove = move
            move = currentNode.NextAction("b", self.table, board, depth)
        #self.table.insert(board, v, 0, bestMove, None)
        return maxUtility, bestMove.moveTuple

    def AlphaBetaSearch(self, previousMove, alpha=-20000000, beta=20000000,\
                        currentNode=None, maxPlayer=True, depth=0, depthLimit=0, board=None):
        #use transposition table scores only if the values present into the entry
        #is significant
        #score = self.table.lookupScore(board, depth)
        #if not score is None:
        #   return score

        self.statesVisited+=1

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
            #self.table.insert(board, utility, depth, None, None)
            return utility

        # Cut off
        if depth == 0:
            utility = Heuristic.ShannonHeuristic(currentNode, self.table, depth, color, board)
            #self.table.insert(board, utility, depth, None, None)
            return utility

        
        # Max
        if maxPlayer:
            v = -20000000
            bestMove = None
            myPreviousMove = board.previousMove
            move = currentNode.NextAction("b", self.table, board, depth)
            while move != None:
                board.movePiece(move)
                node = ChessNode( move )
                # Use transposition table not to search already visisted states
                entry = self.table.lookup(board)
                if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
                    v = max(v, entry[self.table.SCORE])
                else:
                    v = max(v, self.AlphaBetaSearch( myPreviousMove, alpha, beta, node, False, depth-1, depthLimit, board))
                    #Store exact utility value in table
                    self.table.insert(board, v, depthLimit-depth, None , None)
                #Restore previous state before continuing
                board.undoMove(node.getMove(),myPreviousMove)
                if v >= beta:
                    #self.table.insert(board, None, depth, node.getMove() , None)
                    return v
                if v > alpha:
                    alpha = v
                    bestMove = move
                move = currentNode.NextAction("b", self.table, board, depth)
            self.table.insert(board, v, depthLimit-depth, bestMove , None)
            return v

        # Min
        else:
            v = 20000000
            bestMove = None
            myPreviousMove = board.previousMove
            move = currentNode.NextAction("w", self.table, board, depth)
            while move != None:
                board.movePiece(move)
                node = ChessNode(move)
                # Use transposition table not to search already visisted states
                entry = self.table.lookup(board)
                if entry is not None and depth <= entry[self.table.SEARCH_DEPTH]:
                    v = min(v, entry[self.table.SCORE])
                else:
                    v = min(v, self.AlphaBetaSearch(myPreviousMove, alpha, beta, node, True, depth-1, depthLimit, board))
                    #Store exact utility value in table
                    self.table.insert(board, v, depthLimit-depth, None , None)
                #Restore previous state before continuing
                board.undoMove(node.getMove(),myPreviousMove)
                if v <= alpha:
                    #self.table.insert(board, None, depth, node.getMove() , None)
                    return v
                if v < beta:
                    beta = v
                    bestMove = move
                move = currentNode.NextAction("w", self.table, board, depth)
            self.table.insert(board, v, depthLimit-depth, None , bestMove)
            return v
