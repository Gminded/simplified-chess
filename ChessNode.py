from Heuristic import Heuristic
import copy

class ChessNode:
    def __init__(self, board, copyFlag=True):
        if copyFlag:
            self.board = copy.deepcopy(board)
        else:
            self.board = board

        self.utility = -1
        self.moveTuple = None

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

    def SetMoveTuple(self, tuple):
        self.moveTuple = tuple

    def GetMoveTuple(self):
        return self.moveTuple

    #returns just the number of legal moves (for heuristic quickness) (although it's not fast)
    #def LegalMoves(self, playerColor):
    #    return len(self.board.getAllValidMoves())

    def NextAction(self, player_color, counter, inner, actions, table, lastWasTheBest):

        if not lastWasTheBest and counter == 0 and inner == 1:
            if player_color == "white":
                maxPlayer = False
                my_pieces = copy.copy( self.board.whitePawns )
                my_pieces.append(self.board.whiteKing)
                bestMove = table.lookupMinBestMove(self.board)
            else:
                maxPlayer = True
                my_pieces = copy.copy( self.board.blackPawns )
                my_pieces.append(self.board.blackKing)
                bestMove = table.lookupMaxBestMove(self.board)

            actions = []
            for piece in my_pieces:
                moves = self.board.GetListOfValidMoves(player_color, piece)
                if moves:
                    moves.insert(0, ( piece[0], piece[1]) )
                    actions.append(moves)

            if bestMove != None:
                for move in actions:
                    for pos in move[1:]:
                        if move[0] == bestMove[0] and pos == bestMove[1]:
                            move.remove( bestMove[1] )
                        if len(move) == 1:
                            actions.remove(move)
                lastWasTheBest  = True
                successor = ChessNode(self.board)
                successor.SetMoveTuple(bestMove)
                successor.board.MovePiece(bestMove)
                return successor, counter,actions, inner, lastWasTheBest


        if not actions or counter >= len(actions):
            return None, None, None, None, None

        fromCoords = actions[counter][0]
        toCoords = actions[counter][inner]
        lastWasTheBest = False

        move_tuple = fromCoords, toCoords
        successor = ChessNode(self.board)
        successor.SetMoveTuple(move_tuple)
        successor.board.MovePiece(move_tuple)

        #advance
        if inner < ( len(actions[counter]) - 1):
            inner += 1
        else:
            counter += 1
            inner = 1
        return successor, counter,actions, inner, lastWasTheBest