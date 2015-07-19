from Heuristic import Heuristic
import copy

class ChessNode:
    def __init__(self, board, chessMove):
        self.board = copy.copy(board)
        self.utility = -1
        self.chessMove = chessMove

    def GetState(self):
        return self.board.GetState()

    def GetOldState(self):
        return self.board.GetOldState()

    def SetState(self, board):
        self.board = copy.copy(board)

    def GetUtility(self):
        return self.utility

    def SetUtility(self, utility):
        self.utility = utility

    def getMove(self):
        return self.chessMove

    def setMove(self, chessMove):
        self.chessMove = chessMove

    def NextAction(self, player_color, counter, actions, table, lastWasTheBest):

        if not lastWasTheBest and counter == 0:
            if player_color == "white":
                bestMove = table.lookupMinBestMove(self.board)
            else:
                bestMove = table.lookupMaxBestMove(self.board)

            actions = self.board.getAllValidMoves(player_color)

            if bestMove != None:
                for move in actions.moveTuple:
                    for pos in move[1:]:
                        if move[0] == bestMove[0] and pos == bestMove[1]:
                            move.remove( bestMove[1] )
                        if len(move) == 1:
                            actions.remove(move)
                lastWasTheBest  = True

                successor = ChessNode(self.board, bestMove)
                successor.board.MovePiece(bestMove)
                return successor, counter,actions, lastWasTheBest


        if not actions or counter >= len(actions):
            return None, None, None, None, None

        lastWasTheBest = False

        move = actions[counter]
        successor = ChessNode(self.board, move)
        successor.board.MovePiece(move)

        #advance
        counter += 1
        return successor, counter,actions, lastWasTheBest