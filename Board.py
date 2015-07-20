from ChessMove import ChessMove


class Board:
    #player colors
    BLACK='b'
    WHITE='w'

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

    EMPTY = 'e'

    def __init__(self, previousMove):
        self.whiteKing = [7,4] # the white king coordinates
        self.blackKing = [0,4]
        self.whitePawns = [] # all of the white pawns coordinates expressed as lists
        self.blackPawns = []
        self.previousMove = previousMove

        for col in range(8):
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
        return self.EMPTY

    #apply the move chessMove to the chessboard
    def movePiece(self, chessMove):
        #this is just impossible to reach
        #but still useful because it gives semantic to chessMove
        if not self._isPossibleMove(chessMove):
            return False

        fromPos = chessMove.getFromPos()
        toPos = chessMove.getToPos()
        toPosPiece = self.getPiece(toPos)
        pieceType = chessMove.pieceType
        moveType = chessMove.moveType

        if pieceType == self.WHITEKING:
            self.whiteKing = toPos
            if moveType == chessMove.CAPTURE:
                self.blackPawns.remove(toPos)
        elif pieceType == self.BLACKKING:
            self.blackKing = toPos
            if moveType == chessMove.CAPTURE:
                self.whitePawns.remove(toPos)
        elif pieceType == self.BLACKPAWN:
            self.blackPawns.remove(fromPos)
            self.blackPawns.append(toPos)
            if moveType == chessMove.CAPTURE:
                self.whitePawns.remove(toPos)
            elif moveType == chessMove.ENPASSANT_CAPTURE:
                self.whitePawns.remove( [toPos[0] - self.BLACKDIRECTION, toPos[1]] )
        else:
            self.whitePawns.remove(fromPos)
            self.whitePawns.append(toPos)
            if moveType == chessMove.CAPTURE:
                self.blackPawns.remove(toPos)
            elif moveType == chessMove.ENPASSANT_CAPTURE:
                self.blackPawns.remove( [toPos[0] - self.WHITEDIRECTION, toPos[1]] )
        return toPosPiece

    #It's the opposite of movePiece: it restores the state before a move
    def undoMove(self,move,previousMove):
        fromPos=move.moveTuple[0]
        toPos=move.moveTuple[1]
        piece=move.pieceType
        moveType=move.moveType

        self.previousMove=previousMove
        # Always move the piece back to its place, for any move!
        if self.BLACKKING in piece:
            self.blackKing=fromPos
        elif self.WHITEKING in piece:
            self.whiteKing=fromPos
        elif self.BLACKPAWN in piece:
            self.blackPawns.remove(toPos)
            self.blackPawns.append(fromPos)
        elif self.WHITEPAWN in piece:
            self.whitePawns.remove(toPos)
            self.whitePawns.append(fromPos)

        if moveType == move.CAPTURE:
            if self.BLACK in piece:
                self.whitePawns.append(toPos)
            else:
                self.blackPawns.append(toPos)
        elif moveType == move.ENPASSANT_CAPTURE:
            fromRow=fromPos[0]
            toCol=toPos[1]
            capturedPos=[fromRow,toCol]
            if self.BLACK in piece:
                self.whitePawns.append(capturedPos)
            else:
                self.blackPawns.append(capturedPos)


    #returns True if the move is defined in the chessBoard
    def _isInBoard(self, chessMove):
        toPos = chessMove.getToPos()

        if 0 <= toPos[0] <= 7 and 0 <= toPos[1] <= 7:
            return True
        else:
            return False


    #true if the move is a valid one
    def isValidMove(self, chessMove):
        return self._isPossibleMove(chessMove) and\
               not self._doesMovePutInCheck(chessMove) and self._capturePromoted(chessMove)

    #return True if there is no promoted enemy pawn or if there is and this move captures it.
    #return False otherwise
    def _capturePromoted(self,move):
        myColor = move.pieceType[0]
        if myColor == self.WHITE:
            oppPawns = self.blackPawns
            lastRow = 7
        else:
            oppPawns = self.whitePawns
            lastRow = 0
        #look for an enemy pawn in last line. if there is it must be captured
        for col in range(8):
            if [lastRow, col] in oppPawns:
                if move.getToPos() == [lastRow,col]:
                    return True
                else:
                    return False
        #if there is no enemy pawn in the last line any move is OK
        return True

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
        direction = None
        myPawns = None
        advPawn = None
        advKing = None
        advDirection = None
        toPosPiece = self.getPiece(toPos)
        pieceType = chessMove.pieceType

        #advance or capture with a white pawn or a black pawn
        if self.PAWN in pieceType:
            if self.WHITE in pieceType:
                direction = self.WHITEDIRECTION
                advDirection = self.BLACKDIRECTION
                advPawn = self.BLACKPAWN
                advKing = self.BLACKKING
            elif self.BLACK in pieceType:
                direction = self.BLACKDIRECTION
                advDirection = self.WHITEDIRECTION
                advPawn = self.WHITEPAWN
                advKing = self.WHITEKING

            if fromPosRow + direction == toPosRow:
                if fromPosCol == toPosCol and toPosPiece == self.EMPTY:
                    chessMove.moveType=chessMove.MOVE
                    return True
                elif fromPosCol + 1 == toPosCol:
                    if toPosPiece == advPawn or toPosPiece == advKing:
                        chessMove.moveType=chessMove.CAPTURE
                        return True
                    elif self.previousMove.pieceType == advPawn and\
                            self.previousMove.getToPos() == [ fromPosRow, fromPosCol + 1 ] and\
                            self.previousMove.getFromPos() == [ fromPosRow - advDirection*2, fromPosCol+1 ]:
                        chessMove.moveType=chessMove.ENPASSANT_CAPTURE
                        return True
                elif fromPosCol - 1 == toPosCol:
                    if toPosPiece == advPawn or toPosPiece == advKing:
                        chessMove.moveType=chessMove.CAPTURE
                        return True
                    elif self.previousMove.pieceType == advPawn and\
                            self.previousMove.getToPos() == [ fromPosRow, fromPosCol - 1 ] and\
                            self.previousMove.getFromPos() == [ fromPosRow - advDirection*2, fromPosCol-1 ]:
                        chessMove.moveType=chessMove.ENPASSANT_CAPTURE
                        return True
            #advance by 2
            elif self.BLACK in pieceType and fromPosRow == 1  and\
                 fromPosRow + 2 == toPosRow and fromPosCol == toPosCol and toPosPiece == self.EMPTY:
                if self.blackKing == [fromPosRow+direction,fromPosCol] or self.whiteKing == [fromPosRow+direction,fromPosCol]:
                    return False
                for pawns in self.whitePawns, self.blackPawns:
                    for pawn in pawns:
                        if pawn == [fromPosRow+direction,fromPosCol]:
                            return False
                chessMove.moveType = chessMove.MOVE
                return True
            elif self.WHITE in pieceType and fromPosRow == 6  and fromPosRow - 2 == toPosRow and fromPosCol == toPosCol and toPosPiece == self.EMPTY:
                if self.blackKing == [fromPosRow+direction,fromPosCol] or self.whiteKing == [fromPosRow+direction,fromPosCol]:
                    return False
                for pawns in self.whitePawns, self.blackPawns:
                    for pawn in pawns:
                        if pawn == [fromPosRow+direction,fromPosCol]:
                            return False
                chessMove.moveType = chessMove.MOVE
                return True

            return False

        #advance or capture with the black King or the white King
        if self.KING in pieceType:
            if self.BLACK in pieceType:
                advPawn = self.WHITEPAWN
                myPawns = self.BLACKPAWN
            elif self.WHITE in pieceType:
                advPawn = self.BLACKPAWN
                myPawns = self.WHITEPAWN

            if toPosPiece == myPawns:
                return False

            if toPosPiece == advPawn:
                chessMove.moveType=chessMove.CAPTURE
            elif toPosPiece == myPawns:
                return False
            else:
                chessMove.moveType=chessMove.MOVE

            if fromPosRow == toPosRow and ( fromPosCol - 1 == toPosCol or fromPosCol + 1 == toPosCol ):
                return True
            elif fromPosCol == toPosCol and ( fromPosRow - 1 == toPosRow or fromPosRow + 1 == toPosRow ):
                return True
            elif ( fromPosCol + 1 == toPosCol or fromPosCol - 1 == toPosCol ) and\
                    ( fromPosRow + 1 == toPosRow or fromPosRow - 1 == toPosRow ):
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
        if self.getPiece( [toPosRow + direction, toPosCol + 1] ) in advPieces or\
                self.getPiece( [toPosRow + direction, toPosCol - 1] ) in advPieces:
            return False
        else:
            return True

    def _doesMovePutInCheck(self, chessMove):
        if self.WHITEKING in chessMove.pieceType:
            advPieces = []
            advPieces.append(self.BLACKPAWN)
            advPieces.append(self.BLACKKING)
            return not self._canIMoveTheKing(chessMove, advPieces)
        elif self.BLACKKING in chessMove.pieceType:
            advPieces = []
            advPieces.append(self.WHITEPAWN)
            advPieces.append(self.WHITEKING)
            return not self._canIMoveTheKing(chessMove, advPieces)
        elif self.BLACKPAWN in chessMove.pieceType:
            kingRow = self.blackKing[0]
            kingCol = self.blackKing[1]
            if self.getPiece( [kingRow + self.BLACKDIRECTION, kingCol + 1 ] ) == self.WHITEPAWN or\
                    self.getPiece( [kingRow + self.BLACKDIRECTION, kingCol - 1 ] ) == self.WHITEPAWN:
                return True
        else:
            kingRow = self.whiteKing[0]
            kingCol = self.whiteKing[1]
            if self.getPiece( [kingRow + self.WHITEDIRECTION, kingCol + 1 ] ) == self.BLACKPAWN or\
                    self.getPiece( [kingRow + self.WHITEDIRECTION, kingCol - 1 ] ) == self.BLACKPAWN:
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
        if self.BLACK in color:
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
        col=fromCoords[1]
        if self.KING in piece:
            for r in (-1,0,1):
                for c in (-1,0,1):
                    if not (r == c == 0):
                        move=ChessMove([fromCoords,[row+r,col+c]],piece)
                        if self.isValidMove(move):
                            moves.append(move)
        elif self.PAWN in piece:
            destinations=[]
            if self.BLACK in piece:
                direction=self.BLACKDIRECTION
            else:
                direction=self.WHITEDIRECTION
            for c in [-1,0,1]:
                destinations.append( [row+direction,col+c] )
            destinations.append( [row+2*direction,col] )
            for destination in destinations:
                move=ChessMove( [fromCoords,destination] ,piece)
                if self.isValidMove(move):
                    moves.append(move)
        return moves

    # returns True if the player is in check, false otherwise
    def _isInCheck(self,color):
        if self.BLACK in color:
            king=self.blackKing
            direction=self.BLACKDIRECTION
            oppColor=self.WHITE
            oppPawns=self.whitePawns
            oppKing=self.whiteKing
        else:
            king=self.whiteKing
            direction=self.WHITEDIRECTION
            oppColor=self.BLACK
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

    def _isPlayerPromoting(self, playerColor):
        if playerColor == self.WHITE:
            lastRow = 0
            pawns = self.whitePawns
        else:
            lastRow = 7
            pawns = self.blackPawns

        for col in range(8):
            if [lastRow, col] in pawns:
                return True
        return False


    # returns DEFEAT if the player is defeated,
    # DRAW if the game ends in a draw,
    # CONTINUE otherwise
    def terminalTest(self, playerColor):
        if playerColor == self.WHITE:
            otherPlayer = self.BLACK
        else:
            otherPlayer = self.WHITE
        if not self.getAllValidMoves(playerColor):
            if self._isPlayerPromoting(otherPlayer) or self._isInCheck(playerColor):
                return self.DEFEAT
            else:
                return self.DRAW
        return self.CONTINUE

    def convertToAlgebraicNotationCol(self,col):
        columns=['a','b','c','d','e','f','g','h']
        return columns[col]

    def convertToAlgebraicNotationRow(self,row):
        return str(8-row)
