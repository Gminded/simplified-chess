class ChessMove:
    #TYPES OF MOVES
    CAPTURE = 1
    ENPASSANT_CAPTURE = 2
    MOVE = 3
    def __init__(self, moveTuple, pieceType):
        self.moveTuple = moveTuple
        self.moveType = None
        self.pieceType = pieceType

    def getFromPos(self):
        return self.moveTuple[0]

    def getToPos(self):
        return self.moveTuple[1]

    def getPieceType(self):
        return self.pieceType

    def setMoveType(self, moveType):
        self.moveType = moveType
