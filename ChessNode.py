import copy
from ChessMove import ChessMove

class ChessNode:
    def __init__(self, chessMove):
        self.chessMove = chessMove
        self.moveCounter = 0
        self.lastWasTheBest = False
        self.actions = []

    def getMove(self):
        return self.chessMove

    def setMove(self, chessMove):
        self.chessMove = chessMove

    def _resetNode(self):
        self.moveCounter = 0
        self.lastWasTheBest = False
        self.actions = []

    def NextAction(self, player_color, table, board):

        if not self.lastWasTheBest and self.moveCounter == 0:
            if player_color == "w":
                bestMove = table.lookupMinBestMove(board)
            else:
                bestMove = table.lookupMaxBestMove(board)

            possible_actions = board.getAllValidMoves(player_color)

            #ordering by type of move
            for action in possible_actions:
                if action.moveType == ChessMove.CAPTURE or action.moveType == ChessMove.ENPASSANT_CAPTURE:
                    self.actions.append(action)
                    possible_actions.remove(action)
            self.actions.extend(possible_actions)

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

                successor = ChessNode(bestMove)
                board.movePiece(bestMove)
                return successor


        if not self.actions or self.moveCounter >= len(self.actions):
            self._resetNode()
            return None

        self.lastWasTheBest = False

        move = self.actions[self.moveCounter]
        successor = ChessNode(move)
        board.movePiece(move)

        #advance
        self.moveCounter += 1
        return successor
