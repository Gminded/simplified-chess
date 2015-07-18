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

        if not self.isInBoard(chessMove) or fromPos == toPos:
            return False

        fromPosRow = fromPos[0]
        fromPosCol = fromPos[1]
        toPosRow = toPos[0]
        toPosCol = toPos[1]
        toPosPiece = self.getPiece(toPos)
        pieceType = chessMove.getPieceType()
        foundPieceType = False

        #var init
        advKing = advPawn = advDirection = direction = None
        foundPieceType = True

        #advance or capture with a white pawn or a black pawn
        for type in WHITEPAWN,BLACKPAWN:
            if type == WHITEPAWN == pieceType:
                direction = WHITEDIRECTION
                advDirection = BLACKDIRECTION
                advPawn = BLACKPAWN
                advKing = BLACKKING
                foundPieceType = True
            elif type == BLACKPAWN == pieceType:
                direction = BLACKDIRECTION
                advDirection = WHITEDIRECTION
                advPawn = WHITEPAWN
                advKing = WHITEKING
                foundPieceType = True

            if not foundPieceType:
                if type == WHITEPAWN:
                    continue
                else:
                    break


            if fromPosRow + direction == toPosRow:
                if fromPosCol == toPosCol and toPosPiece is None:
                    chessMove.setMoveType(MOVE)
                    return True
                elif fromPosCol + 1 == toPosCol:
                    if toPosPiece == advPawn or toPosPiece == advKing:
                        chessMove.setMoveType(CAPTURE)
                        return True
                    elif self.previousMove.getPieceType() == advPawn and self.previousMove.getToPos() == ( fromPosRow, fromPosCol + 1) and self.previousMove.getFromPos() == ( fromPosRow - advDirection*2, fromPosCol+1 ):
                        chessMove.setMoveType(ENPASSANT)
                        return True
                elif fromPosCol - 1 == toPosCol:
                    if toPosPiece == BLACKPAWN or toPosPiece == advKing:
                        chessMove.setMoveType(CAPTURE)
                    elif self.previousMove.getPieceType() == advPawn and self.previousMove.getToPos() == ( fromPosRow, fromPosCol - 1) and self.previousMove.getFromPos() == ( fromPosRow - advDirection*2, fromPosCol-1 ):
                        chessMove.setMoveType(ENPASSANT)
                        return True
            return False

        #advance or capture with the black King or the white King
        for type in WHITEKING,BLACKKING:
            if type == WHITEKING == pieceType:
                advPawn = BLACKPAWN
            elif type == BLACKKING == pieceType:
                advPawn = WHITEPAWN

            if not foundPieceType:
                if type == WHITEKING:
                    continue
                else:
                    break

            if toPosPiece == advPawn:
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

        return False

    def doesMovePutInCheck(self, chessMove):
        advPawn = None
        toPos = chessMove.getToPos()
        toPosRow = toPos[0]
        toPosCol = toPos[1]

        if chessMove.getPieceType() == WHITEKING:
            advPawn = BLACKPAWN
        elif chessMove.getPieceType() == BLACKKING:
            advPawn = WHITEPAWN
        else:
            return False

        if self.getPiece( (toPosRow, toPosCol + 1) ) == advPawn or self.getPiece( (toPosRow, toPosCol - 1) ) == advPawn:
            return True
        else:
            return False



    #TODO
    #generate possible moves
    #get valid list of moves
    #terminal test



