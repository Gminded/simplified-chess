class ChessMove:
    def __init__(self, moveTuple, moveType, pieceType):
        self.moveTuple = moveTuple
        self.moveType = moveType
        self.pieceType = pieceType

    def getFromPos(self):
        return self.moveTuple[0]

    def getToPos(self):
        return self.moveTuple[1]

    def getPieceType(self):
        return self.pieceType

    def setMoveType(self, moveType):
        self.moveType = moveType