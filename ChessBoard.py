#! /usr/bin/env python
import string
import copy

DEFEAT = 'defeat'
DRAW = 'draw'
NONE = 'none'
WON = 'won'

# To make a complete copy of the previous state.
def complete_copy(inList):
    if isinstance(inList, list):
        return list(map(complete_copy, inList))
    else:
        return inList

class ChessBoard:
    def __init__(self, setupType=0):
        self.whiteKing = [7, 4]  # the white king coordinates
        self.blackKing = [0, 4]
        self.whitePawns = []  # all of the white pawns coordinates expressed as lists
        self.blackPawns = []
        for col in range(0, 8):
            self.whitePawns.append([6, col])
            self.blackPawns.append([1, col])

        self.state = [['bK','e','e','e','e','e','e','e'],\
                        ['e','e','wP','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['wK','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e'],\
                        ['e','e','e','e','e','e','e','e']]
                                        
        if setupType == 0:
                self.state[0] = ['e','e','e','e','bK','e','e','e']
                self.state[1] = ['bP','bP','bP','bP','bP','bP','bP','bP']
                self.state[2] = ['e','e','e','e','e','e','e','e']
                self.state[3] = ['e','e','e','e','e','e','e','e']
                self.state[4] = ['e','e','e','e','e','e','e','e']
                self.state[5] = ['e','e','e','e','e','e','e','e']
                self.state[6] = ['wP','wP','wP','wP','wP','wP','wP','wP']
                self.state[7] = ['e','e','e','e','wK','e','e','e']
        self.oldstate = self.state

    def GetState(self):
        return self.state

    def GetOldState(self):
        return self.oldstate
            
    def ConvertMoveTupleListToAlgebraicNotation(self,moveTupleList):        
            newTupleList = []
            for move in moveTupleList:
                    newTupleList.append((self.ConvertToAlgebraicNotation(move[0]),self.ConvertToAlgebraicNotation(move[1])))
            return newTupleList
    
    def ConvertSquareListToAlgebraicNotation(self,list):
            newList = []
            for square in list:
                    newList.append(self.ConvertToAlgebraicNotation(square))
            return newList

    def ConvertToAlgebraicNotation(self,(row,col)):
            #Converts (row,col) to algebraic notation
            #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
            #Algebraic notation starts in the lower left and uses "a..h" for the column.
            return  self.ConvertToAlgebraicNotation_col(col) + self.ConvertToAlgebraicNotation_row(row)
    
    def ConvertToAlgebraicNotation_row(self,row):
            #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
            #Algebraic notation starts in the lower left and uses "a..h" for the column.    
            B = ['8','7','6','5','4','3','2','1']
            return B[row]
            
    def ConvertToAlgebraicNotation_col(self,col):
            #(row,col) format used in Python Chess code starts at (0,0) in the upper left.
            #Algebraic notation starts in the lower left and uses "a..h" for the column.    
            A = ['a','b','c','d','e','f','g','h']
            return A[col]

            
    def GetFullString(self,p):
            if 'b' in p:
                    name = "black "
            else:
                    name = "white "
                    
            if 'P' in p:
                    name = name + "pawn"
            if 'R' in p:
                    name = name + "rook"
            if 'T' in p:
                    name = name + "knight"
            if 'B' in p:
                    name = name + "bishop"
            if 'Q' in p:
                    name = name + "queen"
            if 'K' in p:
                    name = name + "king"
                    
            return name

    
    def MovePiece(self,moveTuple):
            fromRow = moveTuple[0][0]
            fromCol = moveTuple[0][1]
            toRow = moveTuple[1][0]
            toCol = moveTuple[1][1]
            fromCoords=[fromRow,fromCol]
            toCoords = [toRow, toCol]

            self.oldstate = self.state
            self.state = complete_copy(self.state)
            fromPiece = self.state[fromRow][fromCol]
            toPiece = self.state[toRow][toCol]
            fromCoords = [fromRow, fromCol ]
            toCoords = [ toRow, toCol]
            capturedCoords = None

            # en passant
            enpassant = False
            if 'P' in fromPiece and abs(toCol - fromCol) == 1 and 'e' == self.state[toRow][toCol]:
                capturedPiece = self.state[fromRow][toCol]
                capturedCoords = [fromRow,toCol]
                self.state[fromRow][toCol] = 'e'
                if 'b' in capturedPiece:
                    self.blackPawns.remove(capturedCoords)
                else:
                    self.whitePawns.remove(capturedCoords)
                enpassant = True

            # capture
            elif toPiece != 'e':
                if 'b' in toPiece:
                    self.blackPawns.remove(toCoords)
                else:
                    self.whitePawns.remove(toCoords)

            # always update these values
            self.state[toRow][toCol] = fromPiece
            self.state[fromRow][fromCol] = 'e'
            if 'b' in fromPiece:
                if 'P' in fromPiece:
                    self.blackPawns.remove( fromCoords )
                    self.blackPawns.append( toCoords )
                else:
                    self.blackKing=[toRow,toCol]
            else:
                if 'P' in fromPiece:
                    self.whitePawns.remove( fromCoords )
                    self.whitePawns.append( toCoords )
                else:
                    self.whiteKing=[toRow,toCol]

            fromPiece_fullString = self.GetFullString(fromPiece)
            toPiece_fullString = self.GetFullString(toPiece)
            
            if enpassant:
                    messageString = fromPiece_fullString+ " moves from "+self.ConvertToAlgebraicNotation(moveTuple[0])+\
                                                " to "+self.ConvertToAlgebraicNotation(moveTuple[1])+' and captures '+\
                                                self.ConvertToAlgebraicNotation(capturedCoords)+' with en passant!'
            elif toPiece == 'e':
                    messageString = fromPiece_fullString+ " moves from "+self.ConvertToAlgebraicNotation(moveTuple[0])+\
                                                " to "+self.ConvertToAlgebraicNotation(moveTuple[1])
            else:
                    messageString = fromPiece_fullString+ " from "+self.ConvertToAlgebraicNotation(moveTuple[0])+\
                                            " captures "+toPiece_fullString+" at "+self.ConvertToAlgebraicNotation(moveTuple[1])+"!"
            
            #capitalize first character of messageString
            messageString = string.upper(messageString[0])+messageString[1:len(messageString)]
            
            return messageString

# ChessRules

    def GetListOfValidMoves(self, color,fromTuple):
        legalDestinationSpaces = []
        row=fromTuple[0]
        col=fromTuple[1]
        piece = self.state[row][col]
        moves=[]
        if color=='b':
            direction=1
            myKingCoords=self.blackKing
        else:
            direction=-1
            myKingCoords=self.whiteKing
        if color in piece:
            if 'P' in piece:
                if 0 <= row+direction <= 7:
                    moves.append( [row+direction, col] )
                    if 0 <= col - 1 <= 7:
                        moves.append([row+direction, col-1])
                    if 0 <= col + 1 <= 7:
                        moves.append([row+direction, col+1])
                    moves.append([row+direction*2, col])
            elif 'K' in piece:
                addrow=[0]
                if 0 < row: addrow.append(-1)
                if row < 7: addrow.append(1)
                addcol=[0]
                if 0 < col: addcol.append(-1)
                if col < 7: addcol.append(1)
                for r in addrow:
                    for c in addcol:
                        if not (r==0 and c==0):
                            moves.append([row+r, col+c])

        #check enpassant
        if self.IsEnpassantPawn( fromTuple ):
            if color == 'b':
                if col+1 <= 7 and 'P' in self.state[row][col+1] and 'w' in self.state[row][col+1]:
                    moves.append( [ row, col+1 ] )
                if col-1 >= 0 and 'P' in self.state[row][col-1] and 'w' in self.state[row][col-1]:
                    moves.append( [ row, col-1 ] )
            else:
                if col+1 <= 7 and 'P' in self.state[row][col+1] and 'b' in self.state[row][col+1]:
                    moves.append( [ row, col+1 ] )
                if col-1 >= 0 and 'P' in self.state[row][col-1] and 'b' in self.state[row][col-1]:
                    moves.append( [ row, col-1 ] )


        for toTuple in moves:
            if 'K' in piece:
                check=self.DoesMovePutPlayerInCheck(color, toTuple, fromTuple, toTuple)
            else:
                check=self.DoesMovePutPlayerInCheck(color, myKingCoords, fromTuple, toTuple)
            if not check and self._IsCorrectMove(color,fromTuple,toTuple):
                legalDestinationSpaces.append(toTuple)
        return legalDestinationSpaces

    # Less redundant check for correctness
    def _IsCorrectMove(self,color,fromTuple,toTuple):
        fromRow = fromTuple[0]
        fromCol = fromTuple[1]
        toRow = toTuple[0]
        toCol = toTuple[1]
        if not (0 <= toRow and toRow <= 7) or\
           not (0 <= toCol and toCol <= 7):
               return False
        fromPiece = self.state[fromRow][fromCol]
        toPiece = self.state[toRow][toCol]
        if color == 'b':
            enemyColor = 'w'
        else:
            enemyColor = 'b'

        if 'P' in fromPiece:
            #Pawn
            if color == 'b':
                #en passant
                if 'b' in fromPiece and fromRow==4 and abs(toCol-fromCol)==1 and 'e'==self.state[toRow][toCol]:
                    if 'wP' == self.state[fromRow][toCol] and 'e' == self.state[6][toCol] and 'wP' == self.oldstate[6][toCol]:
                        return True
                if fromRow == 1 and toRow == fromRow+2 and toCol == fromCol and toPiece == 'e':
                    #black pawn on starting row can move forward 2 spaces if there is no one directly ahead
                    if self.IsClearPath(fromTuple,toTuple):
                        return True
                if fromRow==toRow-1 and toCol == fromCol and toPiece == 'e':
                    #moving forward one space
                    return True
                if toRow == fromRow+1 and (toCol == fromCol+1 or toCol == fromCol-1) and enemyColor in toPiece:
                    #attacking
                    return True

            elif color == 'w':
                #en passant
                if 'w' in fromPiece and fromRow==3 and abs(toCol-fromCol)==1 and 'e'==self.state[toRow][toCol]:
                    if 'bP' == self.state[fromRow][toCol] and 'e' == self.state[1][toCol] and 'bP' == self.oldstate[1][toCol]:
                        return True
                if fromRow == 6 and toRow == fromRow-2 and toCol == fromCol and toPiece == 'e':
                    #white pawn on starting row can move forward 2 spaces if there is no one directly ahead
                    if self.IsClearPath(fromTuple,toTuple):
                        return True
                if fromRow==toRow+1 and toCol == fromCol and toPiece == 'e':
                    #moving forward one space
                    return True
                if toRow == fromRow-1 and (toCol == fromCol+1 or toCol == fromCol-1) and enemyColor in toPiece:
                    #attacking
                    return True
        elif 'K' in fromPiece:
            if toPiece=='e' or enemyColor in toPiece:
                return True
        return False

    def IsEnpassantPawn(self,coords):
        row=coords[0]
        col=coords[1]
        piece=self.state[row][col]
        enpassant=False #will become true if enpassant is possible
        captLeft=False
        captRight=True
        # left and right of the piece. -1 stands for a square outside of the self.state.
        left = col - 1
        if col + 1 <= 7:
            right = col + 1
        else:
            right = -1
        # The following "if" hell finds if an en passant move is possible.
        if  'P' in piece or 'p' in piece:
            if 'b' in piece and row==4:
                if left != -1 and 'wP' == self.state[row][left] and 'e' == self.state[5][left]:
                    if 'wP' == self.oldstate[6][left] and 'e' == self.state[6][left]: #the pawn moved by 2 squares
                        enpassant=True
                        captLeft=True
                if right != -1 and 'wP' == self.state[row][right] and 'e' == self.state[5][right]:
                    if 'wP' == self.oldstate[6][right] and 'e' == self.state[6][right]: #the pawn moved by 2 squares
                        enpassant=True
                        captRight=True
            elif 'w' in piece and row==3:
                if left != -1 and 'bP' == self.state[row][left] and 'e' == self.state[2][left]:
                    if 'bP' == self.oldstate[0][left] and 'e' == self.state[0][left]: #the pawn moved by 2 squares
                        enpassant=True
                        captLeft=True
                if right != -1 and 'bP' == self.state[row][right] and 'e' == self.state[2][right]:
                    if 'bP' == self.oldstate[0][right] and 'e' == self.state[0][right]: #the pawn moved by 2 squares
                        enpassant=True
                        captRight=True
        return enpassant, captLeft, captRight

    def IsLegalMove(self, color,fromTuple,toTuple):
        #print "IsLegalMove with fromTuple:",fromTuple,"and toTuple:",toTuple,"color = ",color
        fromRow = fromTuple[0]
        fromCol = fromTuple[1]
        toRow = toTuple[0]
        toCol = toTuple[1]
        fromPiece = self.state[fromRow][fromCol]
        toPiece = self.state[toRow][toCol]
        enemyColor = ""

        if color == "b":
                enemyColor = 'w'
        if color == "w":
                enemyColor = 'b'

        if fromTuple == toTuple:
                return False

        if "P" in fromPiece:
            #Pawn
            if color == "b":
                #en passant
                if 'b' in fromPiece and fromRow==4 and toRow==5 and abs(toCol-fromCol)==1 and 'e'==self.state[toRow][toCol]:
                    if 'wP' == self.state[fromRow][toCol] and 'e' == self.state[6][toCol] and 'wP' == self.oldstate[6][toCol]:
                        return True
                if toRow == fromRow+1 and toCol == fromCol and toPiece == 'e':
                        #moving forward one space
                        return True
                if fromRow == 1 and toRow == fromRow+2 and toCol == fromCol and toPiece == 'e':
                        #black pawn on starting row can move forward 2 spaces if there is no one directly ahead
                        if self.IsClearPath(fromTuple,toTuple):
                                return True
                if toRow == fromRow+1 and (toCol == fromCol+1 or toCol == fromCol-1) and enemyColor in toPiece:
                        #attacking
                        return True

            elif color == "w":
                #en passant
                if 'w' in fromPiece and fromRow==3 and toRow==2 and abs(toCol-fromCol)==1 and 'e'==self.state[toRow][toCol]:
                    if 'bP' == self.state[fromRow][toCol] and 'e' == self.state[1][toCol] and 'bP' == self.oldstate[1][toCol]:
                        return True
                if toRow == fromRow-1 and toCol == fromCol and toPiece == 'e':
                        #moving forward one space
                        return True
                if fromRow == 6 and toRow == fromRow-2 and toCol == fromCol and toPiece == 'e':
                        #black pawn on starting row can move forward 2 spaces if there is no one directly ahead
                        if self.IsClearPath(fromTuple,toTuple):
                                return True
                if toRow == fromRow-1 and (toCol == fromCol+1 or toCol == fromCol-1) and enemyColor in toPiece:
                        #attacking
                        return True

        elif "K" in fromPiece:
                #King
                col_diff = toCol - fromCol
                row_diff = toRow - fromRow
                if toPiece == 'e' or enemyColor in toPiece:
                        if abs(col_diff) == 1 and abs(row_diff) == 0:
                                return True
                        if abs(col_diff) == 0 and abs(row_diff) == 1:
                                return True
                        if abs(col_diff) == 1 and abs(row_diff) == 1:
                                return True

        return False #if none of the other "True"s are hit above

    def DoesMovePutPlayerInCheck(self,color,myKingCoords,fromTuple,toTuple):
        # Faster implementation:
        fromRow=fromTuple[0]
        fromCol=fromTuple[1]
        toRow=toTuple[0]
        toCol=toTuple[1]
        row=myKingCoords[0]
        col=myKingCoords[1]
        right = col < 7
        left = 0 < col
        down = row < 7
        up = 0 < row

        # backup values because we are only simulating
        backupFrom=self.state[fromRow][fromCol]
        backupTo=self.state[toRow][toCol]
        #the error of alternating pwns is here! it's because of enpassant
        #the check is incorrect and returns true in the initial state
        #if color+'P' in backupFrom and abs(toCol - fromCol) == 1 and 'e' == self.state[toRow][toCol]\
        enpassant, captLeft, captRight = self.IsEnpassantPawn(fromTuple)
        if enpassant:
            if captLeft and fromCol-toCol == 1 or captRight and toCol-fromCol == 1:
                self.state[fromRow][toCol]='e'
            else:
                enpassant=False
        self.state[fromRow][fromCol]='e'
        self.state[toRow][toCol]=backupFrom

        check=False

        if color=='b':
            if down and right and 'w' in self.state[row+1][col+1]:
                check=True
            elif down and left and 'w' in self.state[row+1][col-1]:
                check=True
            elif down and 'wK'==self.state[row+1][col]:
                check=True
            elif up and left and 'wK'==self.state[row-1][col-1]:
                check=True
            elif up and right and 'wK'==self.state[row-1][col+1]:
                check=True
            elif up and 'wK'==self.state[row-1][col]:
                check=True
            elif right and 'wK'==self.state[row][col+1]:
                check=True
            elif left and 'wK'==self.state[row][col-1]:
                check=True

        elif color=='w':
            if up and right and 'b' in self.state[row-1][col+1]:
                check=True
            elif up and left and 'b' in self.state[row-1][col-1]:
                check=True
            elif up and 'bK'==self.state[row-1][col]:
                check=True
            elif down and left and 'bK'==self.state[row+1][col-1]:
                check=True
            elif down and right and 'bK'==self.state[row+1][col+1]:
                check=True
            elif down and 'bK'==self.state[row+1][col]:
                check=True
            elif right and 'bK'==self.state[row][col+1]:
                check=True
            elif left and 'bK'==self.state[row][col-1]:
                check=True

        # restore backed up values
        if enpassant:
            if color=='b':
                self.state[fromRow][toCol]='wP'
            else:
                self.state[fromRow][toCol]='bP'

        self.state[fromRow][fromCol]=backupFrom
        self.state[toRow][toCol]=backupTo

        return check

    def IsInCheck(self, color):
        # check if 'color' is in check
        # scan through squares for all enemy pieces; if there IsLegalMove to color's king, then return True.
        if color == "b":
            myColor = 'b'
            enemyColor = 'w'
            enemyColorFull = 'w'
            kingTuple = self.blackKing
            advPawns = self.whitePawns
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColorFull = 'b'
            kingTuple = self.whiteKing
            advPawns = self.blackPawns

        # Check if any of enemy player's pieces has a legal move to current player's king
        for piece in advPawns:
            if self.IsLegalMove(enemyColorFull, piece, kingTuple):
                    return True
        return False

    def IsClearPath(self, fromTuple, toTuple):
        # Return true if there is nothing in a straight line between fromTuple and toTuple, non-inclusive
        # Direction could be +/- vertical, +/- horizontal, +/- diagonal
        fromSquare_r = fromTuple[0]
        fromSquare_c = fromTuple[1]
        toSquare_r = toTuple[0]
        toSquare_c = toTuple[1]
        fromPiece = self.state[fromSquare_r][fromSquare_c]

        if abs(fromSquare_r - toSquare_r) <= 1 and abs(fromSquare_c - toSquare_c) <= 1:
            # The base case: just one square apart
            return True
        else:
            if toSquare_r > fromSquare_r and toSquare_c == fromSquare_c:
                # vertical +
                newTuple = (fromSquare_r + 1, fromSquare_c)
            elif toSquare_r < fromSquare_r and toSquare_c == fromSquare_c:
                # vertical -
                newTuple = (fromSquare_r - 1, fromSquare_c)
            elif toSquare_r == fromSquare_r and toSquare_c > fromSquare_c:
                # horizontal +
                newTuple = (fromSquare_r, fromSquare_c + 1)
            elif toSquare_r == fromSquare_r and toSquare_c < fromSquare_c:
                # horizontal -
                newTuple = (fromSquare_r, fromSquare_c - 1)
            elif toSquare_r > fromSquare_r and toSquare_c > fromSquare_c:
                # diagonal "SE"
                newTuple = (fromSquare_r + 1, fromSquare_c + 1)
            elif toSquare_r > fromSquare_r and toSquare_c < fromSquare_c:
                # diagonal "SW"
                newTuple = (fromSquare_r + 1, fromSquare_c - 1)
            elif toSquare_r < fromSquare_r and toSquare_c > fromSquare_c:
                # diagonal "NE"
                newTuple = (fromSquare_r - 1, fromSquare_c + 1)
            elif toSquare_r < fromSquare_r and toSquare_c < fromSquare_c:
                # diagonal "NW"
                newTuple = (fromSquare_r - 1, fromSquare_c - 1)

        if self.state[newTuple[0]][newTuple[1]] != 'e':
            return False
        else:
            return self.IsClearPath(newTuple, toTuple)

    # color is the color of the current player. The function returns DEFEAT if the current player (color)
    # is defeated in this state. This means that in this state the other player has achieved victory.
    # 
    def TerminalTest(self, color):
        promoted=False #true if the opponent promoted a pawn
        canCapture=False #true if we can capture it
        if color=='b':
            myColor='b'
            opponentColor='w'
            startRow=0
        else:
            myColor='w'
            opponentColor='b'
            startRow=7
        for col in range(8):
            if opponentColor+'P' in self.state[startRow][col]:
                promoted=True
                promotedCol=col
        validMoves=[]
        if myColor=='b':
            validMoves.extend(self.GetListOfValidMoves(color, (self.blackKing[0],self.blackKing[1])))
            for pawn in self.blackPawns:
                validMoves.extend(self.GetListOfValidMoves(color, pawn ))
        else:
            validMoves.extend(self.GetListOfValidMoves(color, (self.whiteKing[0], self.whiteKing[1])))
            for pawn in self.whitePawns:
                validMoves.extend(self.GetListOfValidMoves(color, pawn))
        if promoted and [startRow, promotedCol] in validMoves:
            canCapture = True
        if len(validMoves) == 0:
            if self.IsInCheck(color):
                return DEFEAT
            else:
                return DRAW
        if (promoted and not canCapture):
            return DEFEAT
        return NONE #if the game did not end yet