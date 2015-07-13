from random import *
from ChessBoard import *

class ZobristHash:
    def hash(board):
        state = board.state
        h = 0
        for row in range(8):
            for col in range(8):
                if state[row][col] != 'e':
                    piece = self.pieceId[state[row][col]]
                    h = h xor self.zobristTable[row*8+col][piece]
        return h

    pass
