from random import *

class ZobristHash:

    def __init__(self):
        #costants
        self.whitePawn = 1
        self.whiteKing = 2
        self.blackPawn = 3
        self.blackKing = 4
        self.randomBits = 32

        #generate table
        self.zobristTable = None
        seed()
        for i in range(64):
            for j in range(4):
                self.zobristTable[i][j] = getrandbits(self.randomBits)
