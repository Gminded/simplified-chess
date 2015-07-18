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

    # getter and setter methods could be defined as properties
    # bet we are not doing anything special so they are useless
