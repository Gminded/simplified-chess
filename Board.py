from ChessMove import ChessMove

#player colors
BLACK='b'
WHITE='w'

class Board:
    #TERMINAL STATES
    DEFEAT='defeat'
    DRAW='draw'
    CONTINUE='continue'

    #PIECES
    WHITEKING = 'wK'
    WHITEPAWN = 'wP'
    BLACKKING = 'bK'
    BLACKPAWN = 'bP'
    PAWN = 'P'
    KING = 'K'
    WHITEDIRECTION = -1
    BLACKDIRECTION = 1

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
            return self.WHITEKING
        if self.blackKing == posTuple:
            return self.BLACKKING
        if posTuple in self.whitePawns:
            return self.WHITEPAWN
        if posTuple in self.blackPawns:
            return self.BLACKPAWN
        return None

    #apply the move chessMove to the chessboard
    def movePiece(self, chessMove):
        fromPos = chessMove.getFromPos()
        toPos = chessMove.getToPos()
        pieceType = chessMove.pieceType

        if pieceType == self.WHITEKING:
            self.whiteKing = toPos
        elif pieceType == self.BLACKKING:
            self.blackKing = toPos
        elif pieceType == self.BLACKPAWN and fromPos in self.blackPawns:
            self.blackPawns.remove(fromPos)
            self.blackPawns.append(toPos)
        else:
            self.whitePawns.remove(fromPos)
            self.whitePawns.append(toPos)
        #store the previous move
        self.previousMove = chessMove

    #returns True if the move is defined in the chessBoard
    def _isInBoard(self, chessMove):
        toPos = chessMove.getToPos()

        if 0 <= toPos[0] <= 7 and 0 <= toPos[1] <= 7:
            return True
        else:
            return False


    #true if the move is a valid one
    def isValidMove(self, chessMove):
        return self._isPossibleMove(chessMove) and self._doesMovePutInCheck(chessMove)

    # checks if the move is correct but ignores the fact that
    # it could put the player in check
    def _isPossibleMove(self,chessMove):
        fromPos = chessMove.getFromPos()
        toPos = chessMove.getToPos()

        if not self._isInBoard(chessMove) or fromPos == toPos:
            return False

        fromPosRow = fromPos[0]
        fromPosCol = fromPos[1]
        toPosRow = toPos[0]
        toPosCol = toPos[1]
        toPosPiece = self.getPiece(toPos)
        pieceType = chessMove.pieceType
        foundPieceType = False

        #var init
        advKing = advPawn = advDirection = direction = None
        foundPieceType = True

        #advance or capture with a white pawn or a black pawn
        for type in self.WHITEPAWN,self.BLACKPAWN:
            if type == self.WHITEPAWN == pieceType:
                direction = self.WHITEDIRECTION
                advDirection = self.BLACKDIRECTION
                advPawn = self.BLACKPAWN
                advKing = self.BLACKKING
                foundPieceType = True
            elif type == self.BLACKPAWN == pieceType:
                direction = self.BLACKDIRECTION
                advDirection = self.WHITEDIRECTION
                advPawn = self.WHITEPAWN
                advKing = self.WHITEKING
                foundPieceType = True

            if not foundPieceType:
                if type == self.WHITEPAWN:
                    continue
                else:
                    break


            if fromPosRow + direction == toPosRow:
                if fromPosCol == toPosCol and toPosPiece is None:
                    chessMove.moveType=chessMove.MOVE
                    return True
                elif fromPosCol + 1 == toPosCol:
                    if toPosPiece == advPawn or toPosPiece == advKing:
                        chessMove.moveType=chessMove.CAPTURE
                        return True
                    elif self.previousMove.pieceType == advPawn and self.previousMove.getToPos() == ( fromPosRow, fromPosCol + 1) and self.previousMove.getFromPos() == ( fromPosRow - advDirection*2, fromPosCol+1 ):
                        chessMove.moveType=chessMove.ENPASSANT_CAPTURE
                        return True
                elif fromPosCol - 1 == toPosCol:
                    if toPosPiece == self.BLACKPAWN or toPosPiece == advKing:
                        chessMove.moveType=chessMove.CAPTURE
                    elif self.previousMove.pieceType == advPawn and self.previousMove.getToPos() == ( fromPosRow, fromPosCol - 1) and self.previousMove.getFromPos() == ( fromPosRow - advDirection*2, fromPosCol-1 ):
                        chessMove.moveType=chessMove.ENPASSANT
                        return True
            return False

        #advance or capture with the black King or the white King
        for type in self.WHITEKING,self.BLACKKING:
            if type == self.WHITEKING == pieceType:
                advPawn = self.BLACKPAWN
            elif type == self.BLACKKING == pieceType:
                advPawn = self.WHITEPAWN

            if not foundPieceType:
                if type == self.WHITEKING:
                    continue
                else:
                    break

            if toPosPiece == advPawn:
                chessMove.moveType=chessMove.CAPTURE
            else:
                chessMove.moveType=chessMove.MOVE

            if fromPosRow == toPosRow and ( fromPosCol - 1 == toPosCol or fromPosCol + 1 == toPosCol ):
                return True
            elif fromPosCol == toPosCol and ( fromPosRow - 1 == toPosRow or fromPosRow + 1 == toPosRow ):
                return True
            elif ( fromPosCol + 1 == toPosCol or fromPosCol - 1 == toPosCol ) and ( fromPosRow + 1 == toPosRow or fromPosRow - 1 == toPosRow ):
                return True
            return False

        return False

    def _canIMoveTheKing(self, chessMove, advPieces):
        if self.BLACKPAWN in advPieces:
            direction = self.WHITEDIRECTION
        else:
            direction = self.BLACKDIRECTION
        toPos = chessMove.getToPos()
        toPosRow = toPos[0]
        toPosCol = toPos[1]
        if self.getPiece( (toPosRow + direction, toPosCol + 1) ) in advPieces or self.getPiece( (toPosRow + direction, toPosCol - 1) ) in advPieces:
            return False
        else:
            return True

    def _doesMovePutInCheck(self, chessMove):
        if chessMove.pieceType == self.WHITEKING:
            advPieces = []
            advPieces.append(self.BLACKPAWN)
            advPieces.append(self.BLACKKING)
            return not self._canIMoveTheKing(chessMove, advPieces)
        elif chessMove.pieceType == self.BLACKKING:
            advPieces = []
            advPieces.append(self.WHITEPAWN)
            advPieces.append(self.WHITEKING)
            return not self._canIMoveTheKing(chessMove, advPieces)
        elif chessMove.pieceType == self.BLACKPAWN:
            kingRow = self.blackKing[0]
            kingCol = self.blackKing[1]
            if self.getPiece( (kingRow + self.BLACKDIRECTION, kingCol + 1 ) ) == self.WHITEPAWN or self.getPiece( (kingRow + self.BLACKDIRECTION, kingCol - 1 ) ) == self.WHITEPAWN:
                return True
        else:
            kingRow = self.whiteKing[0]
            kingCol = self.whiteKing[1]
            if self.getPiece( (kingRow + self.WHITEDIRECTION, kingCol + 1 ) ) == self.BLACKPAWN or self.getPiece( (kingRow + self.WHITEDIRECTION, kingCol - 1 ) ) == self.BLACKPAWN:
                return True
        return False




    # Returns the chessboard represented as a string matrix. Each
    def getWholeState(self):
        state=[]
        for row in range(8):
            state.append(['e','e','e','e','e','e','e','e'])
        row,col=self.whiteKing
        state[row][col]='wK'
        row,col=self.blackKing
        state[row][col]='bK'
        for row,col in self.whitePawns:
            state[row][col]='wP'
        for row,col in self.blackPawns:
            state[row][col]='bP'

        return state

    # Returns a list with all valid moves for a player
    def getAllValidMoves(self,color):
        if BLACK in color:
            king=self.blackKing
            pawns=self.blackPawns
            direction=self.BLACKDIRECTION
        else:
            king=self.whiteKing
            pawns=self.whitePawns
            direction=self.WHITEDIRECTION
        moves=[]
        # add the king coordinates
        moves.extend(self.getListOfValidMoves(color+self.KING,king))
        for pawn in pawns:
            moves.extend(self.getListOfValidMoves(color+self.PAWN,pawn))
        return moves

    # Returns a list with all the valid moves for a given piece
    def getListOfValidMoves(self,piece,fromCoords):
        moves=[]
        row=fromCoords[0]
        col=fromCoords[0]
        if self.KING in piece:
            for r in (-1,0,1):
                for c in (-1,0,1):
                    if not (r == c == 0):
                        move=ChessMove((fromCoords,(row+r,col+c)),piece)
                        if self.isValidMove(move):
                            moves.append(move)
        elif self.PAWN in piece:
            destinations=[]
            if BLACK in piece:
                direction=self.BLACKDIRECTION
            else:
                direction=self.WHITEDIRECTION
            for c in [-1,0,1]:
                destinations.append((row+direction,col+c))
            destinations.append((row+2*direction,col))
            for destination in destinations:
                move=ChessMove((fromCoords,destination),piece)
                if self.isValidMove(move):
                    moves.append(move)
        return moves

    # returns True if the player is in check, false otherwise
    def _isInCheck(self,color):
        if BLACK in color:
            king=self.blackKing
            direction=self.BLACKDIRECTION
            oppColor=WHITE
            oppPawns=self.whitePawns
            oppKing=self.whiteKing
        else:
            king=self.whiteKing
            direction=self.WHITEDIRECTION
            oppColor=BLACK
            oppPawns=self.blackPawns
            oppKing=self.blackKing
        row=king[0]
        col=king[1]
        if (row+direction, col-1) in oppPawns or (row+direction,col+1) in oppPawns:
            return True
        for r in [-1,0,1]:
            for c in [-1,0,1]:
                if (row+r, col+c) == oppKing:
                    return True
        return False

    # returns DEFEAT if the player is defeated,
    # DRAW if the game ends in a draw,
    # CONTINUE otherwise
    def terminalTest(self, playerColor):
        if not self.getAllValidMoves(playerColor):
            if self._isInCheck(playerColor):
                return self.DEFEAT
            else:
                return self.DRAW
        return self.CONTINUE
