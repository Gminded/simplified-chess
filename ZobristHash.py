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

        #generate table
        self.zobristTable = [ [ 0 for x in range(4) ] for x in range(64) ]
        for i in range(64):
            for j in range(4):
                self.zobristTable[i][j] = SystemRandom().getrandbits(self.randomBits)

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

    def insertUtility(self, board, utility, depth, maxBestMove, minBestMove):
        key = self.hash(board)
        ret = self.lookup( board )
        if ret != None:
            if depth > ret[1]:
                if not maxBestMove is None:
                    self.hashTable[key] = ret[0], depth, maxBestMove, ret[3]
                elif not minBestMove is None:
                    self.hashTable[key] = ret[0], depth, ret[2], minBestMove
            if not utility is None:
                self.hashTable[key] = utility, ret[1], ret[2], ret[3]
        else:
            self.hashTable[key] = utility, depth, maxBestMove, minBestMove

    def lookupMaxBestMove(self, board):
        key = self.hash(board)
        if key in self.hashTable:
            return self.hashTable[key][2]
        else:
            return None

    def lookupMinBestMove(self, board):
        key = self.hash(board)
        if key in self.hashTable:
            return self.hashTable[key][3]
        else:
            return None

    def lookup(self, board):
        key = self.hash(board)
        if key in self.hashTable:
            return self.hashTable[key]
        else:
            return None
