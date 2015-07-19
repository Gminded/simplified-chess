import copy

class ChessNode:
    def __init__(self, board, chessMove):
        self.board = copy.deepcopy(board)
        self.utility = -1
        self.chessMove = chessMove
        self.moveCounter = 0
        self.lastWasTheBest = False
        self.actions = None

    def GetState(self):
        return self.board.GetState()

    def GetOldState(self):
        return self.board.GetOldState()

    def SetState(self, board):
        self.board = copy.deepcopy(board)

    def GetUtility(self):
        return self.utility

    def SetUtility(self, utility):
        self.utility = utility

    def getMove(self):
        return self.chessMove

    def setMove(self, chessMove):
        self.chessMove = chessMove

    def resetNode(self):
        self.moveCounter = 0
        self.lastWasTheBest = False
        self.actions = None

    def NextAction(self, player_color, table):

        if not self.lastWasTheBest and self.moveCounter == 0:
            if player_color == "w":
                bestMove = table.lookupMinBestMove(self.board)
            else:
                bestMove = table.lookupMaxBestMove(self.board)

            self.actions = self.board.getAllValidMoves(player_color)

            if bestMove != None:
                bestMoveCoords = bestMove.moveTuple
                for move in self.actions:
                    moveCoords = move.moveTuple
                    for pos in moveCoords[1:]:
                        if moveCoords[0] == bestMoveCoords[0] and pos == bestMoveCoords[1]:
                            moveCoords.remove( bestMoveCoords[1] )
                        if len(moveCoords) == 1:
                            self.actions.remove(move)
                self.lastWasTheBest  = True

            successor = ChessNode(self.board, bestMove)
            successor.board.movePiece(bestMove)
            return successor


        if not self.actions or self.moveCounter >= len(self.actions):
            return None

        self.lastWasTheBest = False

        move = self.actions[self.moveCounter]
        successor = ChessNode(self.board, move)
        successor.board.movePiece(move)

        #advance
        self.moveCounter += 1
        return successor
