#!/usr/bin/python2.7

from ChessBoard import *
from ChessPlayer import ChessPlayer
from ChessGUI_pygame import ChessGUI_pygame
from ChessAI import ChessAI
from ChessNode import ChessNode
from ChessGameParams import TkinterGameSetupParams


class PythonChessMain:
    def __init__(self):
        self.Board = ChessBoard(0)

    def SetUp(self):
        # players set up
        self.player = [0, 0]
        self.player[0] = ChessPlayer("Human", "white")
        self.player[1] = ChessAI("AI", "black")
        self.treeDepth = 2
        # GUI setup
        self.guitype = 'pygame'
        GameParams = TkinterGameSetupParams()
        (player1Name, player1Color, player1Type, player2Name, player2Color, player2Type, self.treeDepth) = GameParams.GetGameSetupParams()
        self.Gui = ChessGUI_pygame(self.Board, self.treeDepth)
        self.player = [0, 0]
        if player1Type == 'human':
            self.player[0] = ChessPlayer(player1Name, player1Color)
        elif player1Type == 'AI':
            self.player[0] = ChessAI(player1Name, player1Color)

        if player2Type == 'human':
            self.player[1] = ChessPlayer(player2Name, player2Color)
        elif player2Type == 'AI':
            self.player[1] = ChessAI(player2Name, player2Color)

        if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
            self.AIvsAI = True
        else:
            self.AIvsAI = False


    def MainLoop(self):
        currentPlayerIndex = 0
        turnCount = 0
        currentNode = ChessNode(self.Board, copyFlag=False)  # setup initial node
        while NONE == self.Board.TerminalTest(self.player[currentPlayerIndex].color):
            realBoard = self.Board
            board = self.Board.GetState()
            currentColor = self.player[currentPlayerIndex].GetColor()
            baseMsg = "TURN %s - %s (%s)" % (str(turnCount), self.player[currentPlayerIndex].GetName(), currentColor)
            self.Gui.PrintMessage("-----%s-----" % baseMsg)
            self.Gui.Draw(board)
            # hardcoded so that player 1 is always white
            if currentColor == 'white':
                turnCount = turnCount + 1
            # PLAY TIME
            if self.player[currentPlayerIndex].GetType() == 'AI':
                moveTuple = self.player[currentPlayerIndex].GetMove(currentNode)
            else:
                moveTuple = self.Gui.GetPlayerInput(realBoard, currentColor)

            moveReport = self.Board.MovePiece(moveTuple)
            self.Gui.PrintMessage(moveReport)
            # END OF PLAY TIME
            currentPlayerIndex = (currentPlayerIndex + 1) % 2  # this will cause the currentPlayerIndex to toggle between 1 and 0

        termination = self.Board.TerminalTest(self.player[currentPlayerIndex].color)
        if termination == DEFEAT:
            winnerIndex = (currentPlayerIndex + 1) % 2
            self.Gui.PrintMessage(
                self.player[winnerIndex].GetName() + " (" + self.player[winnerIndex].GetColor() + ") won the game!")
        else:
            self.Gui.PrintMessage('The game ends with a draw!')
        self.Gui.EndGame(self.Board.GetState())


game = PythonChessMain()
game.SetUp()
game.MainLoop()
