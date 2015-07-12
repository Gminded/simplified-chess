from ChessRules import ChessRules

class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, playerColor):
        rules = ChessRules()

        #Heuristic values
        playerEnpassant = 0
        adversaryEnpassant = 0
        promotion = 0
        checkMate = 0
        playerKing = None
        adversaryKing = None
        playerPawns = []
        adversaryPawns = []
        playerMoves = 0
        adversaryMoves = 0

        #board state
        board = node.GetState()
        oldboard = node.GetOldState()

        #checking possible states
        if playerColor == "b":
            adversaryColor = "w"
        else:
            adversaryColor = "b"
        row_no = 0
        col_no = 0
        for row in board:
            for column in row:
                if column == playerColor+"P":
                    playerPawns.append( (row_no, col_no) )
                elif column == playerColor+"K":
                    playerKing = ( row_no, col_no )
                elif column == adversaryColor+"P":
                    adversaryPawns.append( (row_no, col_no) )
                elif column == adversaryColor+"K":
                    adversaryKing = ( row_no, col_no )

                col_no += 1
            # advance row and clear column number
            row_no += 1
            col_no = 0

        #Checking enpassant
        for pawn in playerPawns:
            if rules.IsEnpassantPawn(board, oldboard):
                playerEnpassant += 1
        for pawn in adversaryPawns:
            if rules.IsEnpassantPawn(oldboard, board):
                adversaryEnpassant += 1

        #Checking


import ChessBoard
import ChessNode
if __name__=="__main__":
    board = ChessBoard.ChessBoard()
    node = ChessNode.ChessNode(board.GetState(), board.GetState())
    Heuristic.ShannonHeuristic(node, "b")