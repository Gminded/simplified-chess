#!/usr/bin/python2.7

from Board import *
from ChessPlayer import ChessPlayer
from ChessGUI_pygame import ChessGUI_pygame
from ChessAI import ChessAI
from ChessNode import ChessNode
from ChessGameParams import TkinterGameSetupParams


class PythonChessMain:
    def __init__(self):
        #set an invalid but harmless move as the previous move
        self.board = Board(ChessMove(((0,0),(0,0)), 'bK'))

    def SetUp(self):
        # players set up
        self.player = [0, 0]
        self.player[0] = ChessPlayer("Human", "w")
        self.player[1] = ChessAI("AI", "b")
        self.AIThinkTime = 10
        # GUI setup
        self.guitype = 'pygame'
        GameParams = TkinterGameSetupParams()
        (player1Name, player1Color, player1Type, player2Name, player2Color, player2Type, self.AIThinkTime) = GameParams.GetGameSetupParams()
        self.Gui = ChessGUI_pygame(self.board)
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
        while self.board.CONTINUE == self.board.terminalTest(self.player[currentPlayerIndex].color):
            board = self.board.getWholeState()
            currentColor = self.player[currentPlayerIndex].GetColor()
            baseMsg = "TURN %s - %s (%s)" % (str(turnCount), self.player[currentPlayerIndex].GetName(), currentColor)
            self.Gui.PrintMessage("-----%s-----" % baseMsg)
            self.Gui.Draw(board)
            # hardcoded so that player 1 is always white
            if currentColor == 'w':
                turnCount = turnCount + 1
            # PLAY TIME
            if self.player[currentPlayerIndex].GetType() == 'AI':
                moveTuple, self.board = self.player[currentPlayerIndex].GetMove(self.board, self.AIThinkTime)
            else:
                moveTuple = self.Gui.GetPlayerInput(self.board, currentColor)
            move = ChessMove(moveTuple, board[moveTuple[0][0]][moveTuple[0][1]])
            self.board.movePiece(move)
            moveReport = self.Gui.moveMessage(move,self.board,state=board)
            self.Gui.PrintMessage(moveReport)
            # END OF PLAY TIME
            currentPlayerIndex = (currentPlayerIndex + 1) % 2  # this will cause the currentPlayerIndex to toggle between 1 and 0

        termination = self.board.terminalTest(self.player[currentPlayerIndex].color)
        if termination == self.board.DEFEAT:
            winnerIndex = (currentPlayerIndex + 1) % 2
            self.Gui.PrintMessage(
                self.player[winnerIndex].GetName() + " (" + self.player[winnerIndex].GetColor() + ") won the game!")
        elif termination == self.board.DRAW:
            self.Gui.PrintMessage('The game ends with a draw!')
        self.Gui.EndGame(self.board.getWholeState())


game = PythonChessMain()
game.SetUp()
game.MainLoop()
