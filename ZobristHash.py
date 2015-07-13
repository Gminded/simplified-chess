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
        for i in xrange(self.hashTableLimit):
            self.hashTable[i] = None

    def hash(self, board):
        state = board.state
        h = 0
        for row in range(8):
            for col in range(8):
                if state[row][col] != 'e':
                    piece = self.pieceId[state[row][col]]
                    h = h ^ self.zobristTable[row*8+col][piece]
        return h

    def insertUtility(self, board, utility):
        key = self.hash(board)
        if not key in self.hashTable:
            self.hashTable[key] = utility

    def lookup(self, board):
        key = self.hash(board)
        if key in self.hashTable:
            return self.hashTable[key]
        else:
            return None