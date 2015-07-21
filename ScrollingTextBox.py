#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ScrollingTextBox.py
 Description:  Uses pygame to draw a scrolling text box, which is 
    incorporated in the ChessGUI_pygame class.

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
import pygame
import string

class ScrollingTextBox:
    def __init__(self,screen,xmin,xmax,ymin,ymax, hidpi_factor):
        self.screen = screen
        pygame.font.init()
        self.fontDefault = pygame.font.Font( None, 20*hidpi_factor )

        self.xmin = xmin
        self.xmax = xmax
        self.xPixLength = xmax - xmin
        self.ymin = ymin
        self.ymax = ymax
        self.yPixLength = ymax - ymin

        #max lines in text box is a function of ymin..ymax
        (width,height) = self.fontDefault.size('A')#width seems variable, but height is constant for most fonts (true?)
        self.lineHeight = height
        self.maxLines = self.yPixLength / self.lineHeight
        #print "Height is",height, "so maxLines is", self.maxLines

        #list of lines starts out empty
        self.lines = []

    def getFullString(self,piece):
        if 'b' in piece:
            name = "black "
        else:
            name = "white "
        if 'P' in piece:
            name = name + "pawn"
        if 'R' in piece:
            name = name + "rook"
        if 'T' in piece:
            name = name + "knight"
        if 'B' in piece:
            name = name + "bishop"
        if 'Q' in piece:
            name = name + "queen"
        if 'K' in piece:
            name = name + "king"
        return name

    def moveMessage(self,chessMove,board,state):
        fromCoord=chessMove.getFromPos()
        toCoord=chessMove.getToPos()
        fromPiece_fullString = self.getFullString(chessMove.pieceType)
        fromRow=board.convertToAlgebraicNotationRow(fromCoord[0])
        fromCol=board.convertToAlgebraicNotationCol(fromCoord[1])
        fromString=fromCol+fromRow
        toRow=board.convertToAlgebraicNotationRow(toCoord[0])
        toCol=board.convertToAlgebraicNotationCol(toCoord[1])
        toString=toCol+toRow
        if chessMove.moveType == chessMove.ENPASSANT_CAPTURE:
            capturedString=fromRow+toCol
            messageString = fromPiece_fullString+ " moves from "+fromString+\
                                            " to "+toString+' and captures pawn at '+\
                                            capturedString+' with en passant!'
        elif chessMove.moveType == chessMove.MOVE:
            messageString = fromPiece_fullString+ " moves from "+fromString+\
                                            " to "+toString
        else:
            toPiece_fullString = self.getFullString(state[toCoord[0]][toCoord[1]])
            messageString = fromPiece_fullString+ " from "+fromString+\
                                        " captures "+toPiece_fullString+" at "+toString+"!"

        #capitalize first character of messageString
        messageString = string.upper(messageString[0])+messageString[1:len(messageString)]

        return messageString

    def AddLine(self,newLine):
        #outside functions shouldn't call this...call Add instead (appropriately breaks up message string into lines)
        #there can only be "self.maxLines" in the self.lines array
        #  if textbox is not full, just append the newLine
        #  if textbox is full, pop a line off from the front and add newLine to the back
        if len(self.lines)+1 > self.maxLines:
            self.lines.pop(0) #pop(0) pops off beginning; pop() pops off end
        self.lines.append(newLine)

    def Add(self,message):
        #Break up message string into multiple lines, if necessary
        (width,height) = self.fontDefault.size(message)
        remainder = ""
        if width > self.xPixLength:
            while width > self.xPixLength:
                remainder = message[-1] + remainder
                message = message[0:-1] #chop off last character
                (width,height) = self.fontDefault.size(message)

        if len(remainder) > 0:
            if message[-1].isalnum() and remainder[0].isalnum():
                remainder = message[-1] + remainder
                message = message[0:-1] + '-'
                if message[-2] == ' ':
                    message = message[0:-1] #remove the '-'

        self.AddLine(message)

        if len(remainder) > 0:
            #remove leading spaces
            while remainder[0] == ' ':
                remainder = remainder[1:len(remainder)]
            self.Add(remainder)


    def Draw(self):
        #Draw all lines
        xpos = self.xmin
        ypos = self.ymin
        color = (255,255,255)#white
        antialias = 1 #evidently, for some people rendering text fails when antialiasing is off
        for line in self.lines:
            renderedLine = self.fontDefault.render(line,antialias,color)
            self.screen.blit(renderedLine,(xpos,ypos))
            ypos = ypos + self.lineHeight