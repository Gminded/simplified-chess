from random import *

class ZobristHash:

    def __init__(self, size):
        #costants
        self.pieceId = {
                'wP' : 0,
                'wK' : 1,
                'bP' : 2,
                'bK' : 3
                }
        self.randomBits = 64
        self.hashTableLimit = size
        self.hits = 0
        self.SCORE = 0
        self.SEARCH_DEPTH = 1
        self.MAX_BEST_MOVE = 2
        self.MIN_BEST_MOVE = 3
        self.HAS_MAX = 4
        self.HAS_MIN =5

        #generate table
        self.zobristTable = [ [ 0 for x in range(4) ] for x in range(64) ]
        seed()
        for i in range(64):
            for j in range(4):
                self.zobristTable[i][j] = getrandbits(self.randomBits)

        #init hashTable
        self.hashTable = {}

    def hash(self, board):
        h = 0
        for pawn in board.whitePawns:
            h = h ^ self.zobristTable[ pawn[0]*8 + pawn[1] ][0]
        for pawn in board.blackPawns:
            h = h ^ self.zobristTable[ pawn[0]*8 + pawn[1] ][2]

        h = h ^ self.zobristTable[ board.whiteKing[0]*8 + board.whiteKing[1] ][1]
        h = h ^ self.zobristTable[ board.blackKing[0]*8 + board.blackKing[1] ][3]

        return h

    def insert(self, board, score, searchDepth, maxBestMove, minBestMove):
        key = self.hash(board)
        ret = self.lookup( board )
        if maxBestMove is None:
            hasMax = False
        else:
            hasMax = True
        if minBestMove is None:
            hasMin = False
        else:
            hasMin = True
        if ret != None:
            if searchDepth > ret[self.SEARCH_DEPTH]:
                if hasMax:
                    self.hashTable[key] = [ret[self.SCORE], searchDepth, maxBestMove,\
                                          ret[self.MIN_BEST_MOVE], True, ret[self.HAS_MIN]]
                elif hasMin:
                    self.hashTable[key] = [ret[self.SCORE], searchDepth, ret[self.MAX_BEST_MOVE],\
                                          minBestMove, ret[self.HAS_MAX], True]
                if score is not None:
                    self.hashTable[key][self.SCORE] = score
            elif not ret[self.HAS_MAX]:
                ret[self.MAX_BEST_MOVE]=maxBestMove
            elif not ret[self.MIN_BEST_MOVE]:
                ret[self.MIN_BEST_MOVE]=minBestMove
        else:
            self.hashTable[key] = [score, searchDepth, maxBestMove, minBestMove, hasMax, hasMin]

    def lookup(self, board):
        key = self.hash(board)
        if key in self.hashTable:
            self.hits+=1
            return self.hashTable[key]
        else:
            return None
