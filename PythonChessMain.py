#!/usr/bin/python2.7
"""
 Project: Python Chess
 File name: PythonChessMain.py
 Description:  Chess for player vs. player, player vs. AI, or AI vs. AI.
	Uses Tkinter to get initial game parameters.  Uses Pygame to draw the
	board and pieces and to get user mouse clicks.  Run with the "-h" option
	to get full listing of available command line flags.

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 *******
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 *******
 Version history:

 v 0.7 - 27 April 2009.  Dramatically lowered CPU usage by using
   "pygame.event.wait()" rather than "pygame.event.get()" in
   ChessGUI_pygame.GetPlayerInput().

 v 0.6 - 20 April 2009.  Some compatibility fixes: 1) Class: instead of
   Class(), 2) renamed *.PNG to *.png, 3) rendered text with antialias flag on.
   Also changed exit() to sys.exit(0). (Thanks to tgfcoder from pygame website
   for spotting these errors.)

 v 0.5 - 16 April 2009.  Added new AI functionality - created
   "ChessAI_defense" and "ChessAI_offense."  Created PythonChessAIStats
   class for collecting AI vs. AI stats.  Incorporated Python module
   OptionParser for better command line parsing.

 v 0.4 - 14 April 2009.  Added better chess piece graphics from Wikimedia
   Commons.  Added a Tkinter dialog box (ChessGameParams.py) for getting
   the game setup parameters.  Converted to standard chess notation for
   move reporting and added row/col labels around the board.

 v 0.3 - 06 April 2009.  Added pygame graphical interface.  Includes
   addition of ScrollingTextBox class.

 v 0.2 - 04 April 2009.  Broke up the program into classes that will
   hopefully facilitate easily incorporating graphics or AI play.

 v 0.1 - 01 April 2009.  Initial release.  Draws the board, accepts
   move commands from each player, checks for legal piece movement.
   Appropriately declares player in check or checkmate.

 Possible improvements:
   - Chess Rules additions, ie: Castling, En passant capture, Pawn Promotion
   - Better AI
   - Network play

"""

from ChessBoard import ChessBoard
from ChessPlayer import ChessPlayer
from ChessGUI_pygame import ChessGUI_pygame
from ChessRules import *
from ChessAI import ChessAI
from ChessNode import ChessNode
from ChessGameParams import TkinterGameSetupParams


class PythonChessMain:
    def __init__(self):
        self.Board = ChessBoard(0)
        self.Rules = ChessRules()

    def SetUp(self):
        # players set up
        self.player = [0,0]
        self.player[0] = ChessPlayer("Human", "white")
        self.player[1] = ChessAI("AI", "black")
        # GUI setup
        self.guitype = 'pygame'
        self.Gui = ChessGUI_pygame()
	GameParams = TkinterGameSetupParams()
	(player1Name, player1Color, player1Type, player2Name, player2Color, player2Type) = GameParams.GetGameSetupParams()
        self.player = [0,0]
        if player1Type == 'human':
            self.player[0] = ChessPlayer(player1Name,player1Color)
        elif player1Type == 'randomAI':
            self.player[0] = ChessAI_random(player1Name,player1Color)
        elif player1Type == 'defenseAI':
            self.player[0] = ChessAI_defense(player1Name,player1Color)
        elif player1Type == 'offenseAI':
            self.player[0] = ChessAI_offense(player1Name,player1Color)
                
        if player2Type == 'human':
            self.player[1] = ChessPlayer(player2Name,player2Color)
        elif player2Type == 'randomAI':
            self.player[1] = ChessAI_random(player2Name,player2Color)
        elif player2Type == 'defenseAI':
            self.player[1] = ChessAI_defense(player2Name,player2Color)
        elif player2Type == 'offenseAI':
            self.player[1] = ChessAI_offense(player2Name,player2Color)
                
        if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
            self.AIvsAI = True
        else:
            self.AIvsAI = False

    def MainLoop(self):
        currentPlayerIndex = 0
        turnCount = 0
        currentNode = ChessNode(self.Board.GetState(), self.Board.GetState()) #setup initial node
        while NONE == self.Rules.TerminalTest(self.Board.oldstate,self.Board.GetState(),self.player[currentPlayerIndex].color):
            realBoard = self.Board
            board = self.Board.GetState()
            currentColor = self.player[currentPlayerIndex].GetColor()
            baseMsg = "TURN %s - %s (%s)" % (str(turnCount),self.player[currentPlayerIndex].GetName(),currentColor)
            self.Gui.PrintMessage("-----%s-----" % baseMsg)
            self.Gui.Draw(board)
            # hardcoded so that player 1 is always white
            if currentColor == 'white':
                turnCount = turnCount + 1
            #PLAY TIME
            if self.player[currentPlayerIndex].GetType() == 'AI':
                moveTuple = self.player[currentPlayerIndex].GetMove(currentNode, depth=2,threaded=False, threadTotal=4)
            else:
                moveTuple = self.Gui.GetPlayerInput(realBoard,currentColor)

            moveReport = self.Board.MovePiece(moveTuple)
            currentNode.SetState( self.Board.GetState() ) #new state and remembering old_state
            self.Gui.PrintMessage(moveReport)
            #END OF PLAY TIME
            currentPlayerIndex = (currentPlayerIndex + 1) % 2  # this will cause the currentPlayerIndex to toggle between 1 and 0

        self.Gui.PrintMessage("CHECKMATE!")
        winnerIndex = (currentPlayerIndex + 1) % 2
        self.Gui.PrintMessage(self.player[winnerIndex].GetName() + " (" + self.player[winnerIndex].GetColor() + ") won the game!")
        self.Gui.EndGame(self.Board.GetState())


game = PythonChessMain()
game.SetUp()
game.MainLoop()
