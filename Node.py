from ChessRules import ChessRules
from ChessBoard import ChessBoard
from Heuristic import Heuristic

class Node:
    def __init__(self, state, old_state):
        self.state = state
        self.old_state = old_state
        self.utility = -1

    def availableActions(self, player_color):
        rules = ChessRules()
        board = ChessBoard()
        my_pawns = []
        row_no = 0
        col_no = 0
        for row in self.state:
            for column in row:
                if column[0:1] == player_color[0:1]:
                    my_pawns.append( (row_no, col_no) )
                col_no += 1
            #advance row and clear column number
            row_no += 1
            col_no = 0

        #now we have the list of pawns of the current player
        #Format of actions
        # [ [ (current_pawn_position), (possible_move), (possible_move) ], [ (current_pawn_position), (possible_move) ], ... ]
        #creating nodes and move ordering based on the (approximated) utility value
        actions = []
        successors = []
        for pawn in my_pawns:
            moves =  rules.GetListOfValidMoves( self.old_state, self.state, player_color, pawn)
            moves.insert(0, pawn)
            actions.append( moves )

            #creating nodes
            for i in moves[1:]:
                board.squares = self.state
                move_tuple = moves[0:1], i
                print move_tuple
                board.MovePiece(move_tuple)
                successor = Node(board, self.state)
                Heuristic.HeuristicFunction( successor )

            successors.append( successor )