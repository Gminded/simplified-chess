from ChessRules import ChessRules
from ChessBoard import ChessBoard
from ChessBoard import complete_copy
from Heuristic import Heuristic


class ChessNode:
    def __init__(self, state, old_state):
        self.state = complete_copy(state)
        self.old_state = complete_copy(old_state)
        self.utility = -1
        self.moveTuple = None

    def GetOldState(self):
        return self.old_state

    def GetState(self):
        return self.state

    def SetState(self, state):
        self.old_state = complete_copy(state)
        self.state = complete_copy(state)

    def GetUtility(self):
        return self.utility

    def SetMoveTuple(self, tuple):
        self.moveTuple = tuple

    def GetMoveTuple(self):
        return self.moveTuple

    #return successor nodes
    def Actions(self, player_color, threaded=None, threadIndex=-1, threadTotal=-1):
        rules = ChessRules()
        board = ChessBoard()
        my_pawns = []
        row_no = 0
        col_no = 0
        for row in self.GetState():
            for column in row:
                if column[0:1] == player_color[0:1]:
                    my_pawns.append((row_no, col_no))
                col_no += 1
            # advance row and clear column number
            row_no += 1
            col_no = 0

        # now we have the list of pawns of the current player
        # Format of actions
        # [ [ (current_pawn_position), (possible_move), (possible_move) ], [ (current_pawn_position), (possible_move) ], ... ]
        # creating nodes and move ordering based on the (approximated) utility value
        actions = []
        successors = []
        for pawn in my_pawns:
            moves = rules.GetListOfValidMoves(self.old_state, self.state, player_color, pawn)
            moves.insert(0, pawn)
            actions.append(moves)

            # creating nodes
            for i in moves[1:]:
                board.squares = self.state
                move_tuple = moves[0], i
                board.MovePiece(move_tuple)
                successor = ChessNode(board.squares, self.state)
                successor.SetMoveTuple(move_tuple)
                Heuristic.HeuristicFunction(successor)

                #ordering (descending)
                count = 0
                inserted = False
                if not successors:
                    successors.append(successor)
                else:
                    for k in successors:
                        if successor.utility > k.utility:
                            successors.insert(count, successor )
                            inserted = True
                            break
                        count += 1
                    if not inserted:
                        successors.append(successor)
        if threaded:
            if threadIndex+1 != threadTotal:
                return successors[ threadIndex*threadTotal : len(successors)/threadTotal * (threadIndex+1) ]
            else:
                return successors[ threadIndex*threadTotal :]
        else:
            return successors