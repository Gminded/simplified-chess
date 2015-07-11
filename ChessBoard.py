#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessBoard.py
 Description:  Board layout; contains what pieces are present
        at each square.
        
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
import string

class ChessBoard:
        def __init__(self,setupType=0):
                self.state = [['e','e','e','e','e','e','e','e'],\
                                                ['e','e','e','e','e','e','e','e'],\
                                                ['e','e','e','e','e','e','e','e'],\
                                                ['e','e','e','e','e','e','e','e'],\
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

        # To make a complete copy of the previous state.
        def complete_copy(inList):
            if isinstance(inList, list):
                return list( map(unshared_copy, inList) )
                return inList
        
        def MovePiece(self,moveTuple):
                fromSquare_r = moveTuple[0][0]
                fromSquare_c = moveTuple[0][1]
                toSquare_r = moveTuple[1][0]
                toSquare_c = moveTuple[1][1]

                self.oldstate = complete_copy(self.state)

                fromPiece = self.state[fromSquare_r][fromSquare_c]
                toPiece = self.state[toSquare_r][toSquare_c]

                self.state[toSquare_r][toSquare_c] = fromPiece
                self.state[fromSquare_r][fromSquare_c] = 'e'

                fromPiece_fullString = self.GetFullString(fromPiece)
                toPiece_fullString = self.GetFullString(toPiece)
                
                if toPiece == 'e':
                        messageString = fromPiece_fullString+ " moves from "+self.ConvertToAlgebraicNotation(moveTuple[0])+\
                                                    " to "+self.ConvertToAlgebraicNotation(moveTuple[1])
                else:
                        messageString = fromPiece_fullString+ " from "+self.ConvertToAlgebraicNotation(moveTuple[0])+\
                                                " captures "+toPiece_fullString+" at "+self.ConvertToAlgebraicNotation(moveTuple[1])+"!"
                
                #capitalize first character of messageString
                messageString = string.upper(messageString[0])+messageString[1:len(messageString)]
                
                return messageString
