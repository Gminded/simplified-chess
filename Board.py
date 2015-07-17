#TERMINAL STATES
DEFEAT='defeat'
DRAW='draw'
NONE='none'
WON='won'

#PIECES
WHITEKING = 'wK'
WHITEPAWN = 'wP'
BLACKKING = 'bK'
BLACKPAWN = 'bP'
PAWN = 'P'
KING = 'K'
WHITEDIRECTION = -1
BLACKDIRECTION = 1

#TYPES OF MOVES
CAPTURE = 1
ENPASSANT = 2
MOVE = 3

class Board:
    def __init__(self):
        self.whiteKing = [7,4] # the white king coordinates
        self.blackKing = [0,4]
        self.whitePawns = [] # all of the white pawns coordinates expressed as lists
        self.blackPawns = []
        self.previousMove = None

        for col in range(0,8):
            self.whitePawns.append([6,col])
            self.blackPawns.append([1,col])

    #return what type of piece there is in posTuple (if there is one)
    def getPiece(self, posTuple):
        if self.whiteKing == posTuple:
            return WHITEKING
        if self.blackKing == posTuple:
            return BLACKKING
        if posTuple in self.whitePawns:
            return WHITEPAWN
        if posTuple in self.blackPawns:
            return BLACKPAWN
        return None

    #apply the move chessMove to the chessboard
    def movePiece(self, chessMove):
        fromPos = chessMove.getFromPos()
        toPos = chessMove.getToPos()
        pieceType = chessMove.getPieceType()

        if pieceType == WHITEKING:
            self.whiteKing = toPos
        elif pieceType == BLACKKING:
            self.blackKing = toPos
        elif pieceType == BLACKPAWN and fromPos in self.blackPawns:
            self.blackPawns.remove(fromPos)
            self.blackPawns.append(toPos)
        else:
            self.whitePawns.remove(fromPos)
            self.whitePawns.append(toPos)
        #store the previous move
        self.previousMove = chessMove

    #returns True if the move is defined in the chessBoard
    def isInBoard(self, chessMove):
        toPos = chessMove.getToPos()

        if 0 <= toPos[0] <= 7 and 0 <= toPos[1] <= 7:
            return True
        else:
            return False


    #true if the move is a valid one
    def isValidMove(self, chessMove):

        fromPos = chessMove.getFromPos()
        toPos = chessMove.getToPos()

        if not self.isInBoard(chessMove) and fromPos == toPos:
            return False

        fromPosRow = fromPos[0]
        fromPosCol = fromPos[1]
        toPosRow = toPos[0]
        toPosCol = toPos[1]
        pieceType = chessMove.getPieceType()
        toPosPiece = self.getPiece(toPos)

        #advance or capture with a white pawn
        if pieceType == WHITEPAWN:
            if fromPosRow + WHITEDIRECTION == toPosRow:
                if fromPosCol == toPosCol and toPosPiece is None:
                    chessMove.setMoveType(MOVE)
                    return True
                elif fromPosCol == toPosCol + 1 and ( toPosPiece == BLACKPAWN or toPosPiece == BLACKKING ):
                    chessMove.setMoveType(CAPTURE)
                    return True
                elif fromPosCol == toPosCol - 1 and ( toPosPiece == BLACKPAWN or toPosPiece == BLACKKING ):
                    chessMove.setMoveType(CAPTURE)
                    return True
                ##IMPLEMENT ENPASSANT1
            return False

        #advance or capture with a black pawn
        if pieceType == BLACKPAWN:
            if fromPosRow + BLACKDIRECTION == toPosRow:
                if fromPosCol == toPosCol and self.getPiece(toPos) is None:
                    chessMove.setMoveType(MOVE)
                    return True
                elif fromPosCol == toPosCol + 1 and ( toPosPiece == WHITEPAWN or toPosPiece == WHITEKING ):
                    chessMove.setMoveType(CAPTURE)
                    return True
                elif fromPosCol == toPosCol - 1 and ( toPosPiece == WHITEPAWN or toPosPiece == WHITEKING ):
                    chessMove.setMoveType(CAPTURE)
                    return True
                ##IMPLEMENT ENPASSANT2
            return False

        #advance or capture with the black King
        if pieceType == WHITEKING:
            if toPosPiece == BLACKPAWN:
                chessMove.setMoveType(CAPTURE)
            else:
                chessMove.setMoveType(MOVE)

            if fromPosRow == toPosRow and ( fromPosCol - 1 == toPosCol or fromPosCol + 1 == toPosCol ):
                return True
            elif fromPosCol == toPosCol and ( fromPosRow - 1 == toPosRow or fromPosRow + 1 == toPosRow ):
                return True
            elif ( fromPosCol + 1 == toPosCol or fromPosCol - 1 == toPosCol ) and ( fromPosRow + 1 == toPosRow or fromPosRow - 1 == toPosRow ):
                return True
            return False

        #advance or capture with the white King
        if pieceType == BLACKKING:
            if toPosPiece == WHITEPAWN:
                chessMove.setMoveType(CAPTURE)
            else:
                chessMove.setMoveType(MOVE)

            if fromPosRow == toPosRow and ( fromPosCol - 1 == toPosCol or fromPosCol + 1 == toPosCol ):
                return True
            elif fromPosCol == toPosCol and ( fromPosRow - 1 == toPosRow or fromPosRow + 1 == toPosRow ):
                return True
            elif ( fromPosCol + 1 == toPosCol or fromPosCol - 1 == toPosCol ) and ( fromPosRow + 1 == toPosRow or fromPosRow - 1 == toPosRow ):
                return True
            return False





