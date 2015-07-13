from random import *
from ChessBoard import *

class ZobristHash:

    def __init__(self):
        #costants
        self.pieceId = {
                'wP' : 1,
                'wK' : 2,
                'bP' : 3,
                'bK' : 4
                }
        self.randomBits = 32
        self.hashTableLimit = 2**24

        #generate table
        self.zobristTable = [ [ 0 for x in range(4) ] for x in range(64) ]
        seed()
        for i in range(64):
            for j in range(4):
                self.zobristTable[i][j] = getrandbits(self.randomBits)

        #init hashTable
        self.hashTable = {}
        for i in xrange(2**24):
            self.hashTableSize = None

    def hash(self, board):
        state = board.state
        h = 0
        for row in range(8):
            for col in range(8):
                if state[row][col] != 'e':
                    piece = self.pieceId[state[row][col]]
                    h = h ^ self.zobristTable[row*8+col][piece]
        return h

    def insert(self, key, tuple):
        self.hashTableSize[key] = tuple

    def lookup(self, key):
        if key in self.hashTable
            return self.hashTable[key]
        else:
            return None


