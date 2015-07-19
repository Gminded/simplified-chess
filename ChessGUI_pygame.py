#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessGUI_pygame.py
 Description:  Uses pygame (http://www.pygame.org/) to draw the
    chess board, as well as get user input through mouse clicks.
    The chess tile graphics were taken from Wikimedia Commons,
    http://commons.wikimedia.org/wiki/File:Chess_tile_pd.png

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

import pygame
import os
import sys
from pygame.locals import *
from ScrollingTextBox import ScrollingTextBox
from Board import *

class ChessGUI_pygame:
    def __init__(self,board):
        os.environ['SDL_VIDEO_CENTERED'] = '1' #should center pygame window on the screen
        pygame.init()
        self.board = board
        self.hidpi_factor = pygame.display.Info().current_h / 600
        self.screen = pygame.display.set_mode((850*self.hidpi_factor, 600*self.hidpi_factor), pygame.DOUBLEBUF)
        self.boardStart_x = 50*self.hidpi_factor
        self.boardStart_y = 50*self.hidpi_factor
        pygame.display.set_caption('Simplified Chess')

        self.textBox = ScrollingTextBox(self.screen,525*self.hidpi_factor,825*self.hidpi_factor,50*self.hidpi_factor,450*self.hidpi_factor, self.hidpi_factor)
        self.LoadImages()
        self.fontDefault = pygame.font.Font( None, 20*self.hidpi_factor )




    def LoadImages(self):
        self.square_size = 50*self.hidpi_factor
        self.white_square = pygame.image.load(os.path.join("images","white_square.png")).convert()
        self.white_square = pygame.transform.scale(self.white_square, (self.square_size,self.square_size))
        self.brown_square = pygame.image.load(os.path.join("images","brown_square.png")).convert()
        self.brown_square = pygame.transform.scale(self.brown_square, (self.square_size,self.square_size))
        self.cyan_square = pygame.image.load(os.path.join("images","cyan_square.png")).convert()
        self.cyan_square = pygame.transform.scale(self.cyan_square, (self.square_size,self.square_size))

        self.black_pawn = pygame.image.load(os.path.join("images","Chess_tile_pd.png")).convert()
        self.black_pawn = pygame.transform.scale(self.black_pawn, (self.square_size,self.square_size))
        self.black_king = pygame.image.load(os.path.join("images","Chess_tile_kd.png")).convert()
        self.black_king = pygame.transform.scale(self.black_king, (self.square_size,self.square_size))

        self.white_pawn = pygame.image.load(os.path.join("images","Chess_tile_pl.png")).convert()
        self.white_pawn = pygame.transform.scale(self.white_pawn, (self.square_size,self.square_size))
        self.white_king = pygame.image.load(os.path.join("images","Chess_tile_kl.png")).convert()
        self.white_king = pygame.transform.scale(self.white_king, (self.square_size,self.square_size))

    def PrintMessage(self,message):
        #prints a string to the area to the right of the board
        self.textBox.Add(message)
        self.textBox.Draw()

    def ConvertToScreenCoords(self,chessSquareTuple):
        #converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        (row,col) = chessSquareTuple
        screenX = self.boardStart_x + col*self.square_size
        screenY = self.boardStart_y + row*self.square_size
        return (screenX,screenY)

    def ConvertToChessCoords(self,screenPositionTuple):
        #converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        #x is horizontal, y is vertical
        #(x=0,y=0) is upper-left corner of the screen
        (X,Y) = screenPositionTuple
        row = (Y-self.boardStart_y) / self.square_size
        col = (X-self.boardStart_x) / self.square_size
        return [row,col]


    def Draw(self,board,highlightSquares=[]):
        self.screen.fill((0,0,0))
        self.textBox.Draw()
        boardSize = len(board) #board should be square.  boardSize should be always 8 for chess, but I dislike "magic numbers" :)

        #draw blank board
        current_square = 0
        for r in range(boardSize):
            for c in range(boardSize):
                (screenX,screenY) = self.ConvertToScreenCoords((r,c))
                if current_square:
                    self.screen.blit(self.brown_square,(screenX,screenY))
                    current_square = (current_square+1)%2
                else:
                    self.screen.blit(self.white_square,(screenX,screenY))
                    current_square = (current_square+1)%2

            current_square = (current_square+1)%2

        #draw row/column labels around the edge of the board
        color = (255,255,255)#white
        antialias = 1

        #top and bottom - display cols
        for c in range(boardSize):
            for r in [-1,boardSize]:
                (screenX,screenY) = self.ConvertToScreenCoords((r,c))
                screenX = screenX + self.square_size/2
                screenY = screenY + self.square_size/2
                notation = self.board.convertToAlgebraicNotationCol(c)
                renderedLine = self.fontDefault.render(notation,antialias,color)
                self.screen.blit(renderedLine,(screenX,screenY))

        #left and right - display rows
        for r in range(boardSize):
            for c in [-1,boardSize]:
                (screenX,screenY) = self.ConvertToScreenCoords((r,c))
                screenX = screenX + self.square_size/2
                screenY = screenY + self.square_size/2
                notation = self.board.convertToAlgebraicNotationRow(r)
                renderedLine = self.fontDefault.render(notation,antialias,color)
                self.screen.blit(renderedLine,(screenX,screenY))

        #highlight squares if specified
        for square in highlightSquares:
            (screenX,screenY) = self.ConvertToScreenCoords(square)
            self.screen.blit(self.cyan_square,(screenX,screenY))

        #draw pieces
        for r in range(boardSize):
            for c in range(boardSize):
                (screenX,screenY) = self.ConvertToScreenCoords((r,c))
                if board[r][c] == 'bP':
                    self.screen.blit(self.black_pawn,(screenX,screenY))
                if board[r][c] == 'bK':
                    self.screen.blit(self.black_king,(screenX,screenY))
                if board[r][c] == 'bQ' or board[r][c] == 'bP' and r == 7:
                    self.screen.blit(self.black_queen,(screenX,screenY))
                if board[r][c] == 'wP':
                    self.screen.blit(self.white_pawn,(screenX,screenY))
                if board[r][c] == 'wK':
                    self.screen.blit(self.white_king,(screenX,screenY))
                if board[r][c] == 'wQ' or board[r][c] == 'wP' and r == 0:
                    self.screen.blit(self.white_queen,(screenX,screenY))

        pygame.display.flip()

    def EndGame(self,board):
        self.PrintMessage("Press any key to exit.")
        self.Draw(board) #draw board to show end game status
        pygame.event.set_blocked(MOUSEMOTION)
        while 1:
            e = pygame.event.wait()
            if e.type is KEYDOWN:
                pygame.quit()
                sys.exit(0)
            if e.type is QUIT:
                pygame.quit()
                sys.exit(0)


    def GetPlayerInput(self,board,currentColor):
        #returns ((from_row,from_col),(to_row,to_col))
        state = board.getWholeState()
        fromSquareChosen = 0
        toSquareChosen = 0
        while not fromSquareChosen or not toSquareChosen:
            squareClicked = []
            pygame.event.set_blocked(MOUSEMOTION)
            pygame.event.pump()
            e = pygame.event.wait()
            if e.type is KEYDOWN:
                if e.key is K_ESCAPE:
                    fromSquareChosen = 0
                    fromTuple = []
            if e.type is MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                squareClicked = self.ConvertToChessCoords((mouseX,mouseY))
                if squareClicked[0]<0 or squareClicked[0]>7 or squareClicked[1]<0 or squareClicked[1]>7:
                    squareClicked = [] #not a valid chess square
            if e.type is QUIT: #the "x" kill button
                pygame.quit()
                sys.exit(0)


            if not fromSquareChosen and not toSquareChosen:
                self.Draw(state)
                if squareClicked != []:
                    (r,c) = squareClicked
                    if currentColor == 'black' and 'b' in state[r][c]:
                        if len(self.board.getListOfValidMoves(state[r][c],squareClicked))>0:
                            fromSquareChosen = 1
                            fromTuple = squareClicked
                    elif currentColor == 'white' and 'w' in state[r][c]:
                        if len(self.board.getListOfValidMoves(state[r][c],squareClicked))>0:
                            fromSquareChosen = 1
                            fromTuple = squareClicked

            elif fromSquareChosen and not toSquareChosen:
                moves = self.board.getListOfValidMoves(state[r][c],fromTuple)
                possibleDestinations = []
                for move in moves:
                    moveTuple = move.moveTuple
                    possibleDestinations.append(moveTuple[1]) #take only the destination coordinates
                self.Draw(state,possibleDestinations)
                if squareClicked != []:
                    (r,c) = squareClicked
                    if squareClicked in possibleDestinations:
                        toSquareChosen = 1
                        toTuple = squareClicked
                    elif currentColor == 'black' and 'b' in state[r][c]:
                        if squareClicked == fromTuple:
                            fromSquareChosen = 0
                        elif len(self.board.getListOfValidMoves(state[r][c],squareClicked))>0:
                            fromSquareChosen = 1
                            fromTuple = squareClicked
                        else:
                            fromSquareChosen = 0 #piece is of own color, but no possible moves
                    elif currentColor == 'white' and 'w' in state[r][c]:
                        if squareClicked == fromTuple:
                            fromSquareChosen = 0
                        elif len(self.board.getListOfValidMoves(state[r][c],squareClicked))>0:
                            fromSquareChosen = 1
                            fromTuple = squareClicked
                        else:
                            fromSquareChosen = 0
                    else: #blank square or opposite color piece not in possible destinations clicked
                        fromSquareChosen = 0

        return (fromTuple,toTuple)
