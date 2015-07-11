from ChessRules import ChessRules

class Node:
    def __init__(self, state, old_state):
        self.state = state
        self.old_state = old_state

    def availableActions(self, player_color):
        rules = ChessRules()
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
        actions = []
        for pawn in my_pawns:
            actions.append( rules.GetListOfValidMoves( self.state, player_color, pawn) )

        print actions