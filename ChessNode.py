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

    #returns just the number of legal moves (for heuristic quickness)
    def LegalMoves(self, playerColor):
        if playerColor == "white":
            my_pieces = self.board.whitePawns
            myKing = self.board.whiteKing
        else:
            my_pieces = self.board.blackPawns
            myKing = self.board.blackKing

        #pawn moves counting
        actions = 0
        for piece in my_pieces:
            actions += len( self.board.GetListOfValidMoves(playerColor, piece) )
        #king moves counting
        actions += len( self.board.GetListOfValidMoves(playerColor, myKing) )
        return  actions

    def NextAction(self, player_color, counter, inner, actions, table, lastWasTheBest):

        if not lastWasTheBest and counter == 0 and inner == 1:
            if player_color == "white":
                maxPlayer = False
                my_pieces = copy.copy( self.board.whitePawns )
                my_pieces.append(self.board.whiteKing)
            else:
                maxPlayer = True
                my_pieces = copy.copy( self.board.blackPawns )
                my_pieces.append(self.board.blackKing)

            actions = []
            for piece in my_pieces:
                moves = self.board.GetListOfValidMoves(player_color, piece)
                if moves:
                    moves.insert(0, ( piece[0], piece[1]) )
                    actions.append(moves)

            bestMove, player = table.lookupBestMove(self.board)
            if bestMove != None and maxPlayer == player :
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

    #return successor nodes
    def Actions(self, player_color, table):
        if player_color == "white":
            my_pieces = copy.copy( self.board.whitePawns )
            my_pieces.append(self.board.whiteKing)
        else:
            my_pieces = copy.copy( self.board.blackPawns )
            my_pieces.append(self.board.blackKing)

        # Format of actions
        # [ [ (current_pawn_position), (possible_move), (possible_move) ], [ (current_pawn_position), (possible_move) ], ... ]
        # creating nodes and move ordering based on the (approximated) utility value
        actions = []
        successors = []
        for piece in my_pieces:
            moves = self.board.GetListOfValidMoves(player_color, piece)
            moves.insert(0, piece)
            actions.append(moves)

            # creating nodes
            for i in moves[1:]:
                move_tuple = moves[0], i
                successor = ChessNode(self.board)
                successor.SetMoveTuple(move_tuple)
                successor.board.MovePiece(move_tuple)
                Heuristic.ShannonHeuristic(successor, table)

                #ordering (descending)
                count = 0
                posToInsert = 0
                inserted = False
                if not successors:
                    successors.append(successor)
                else:
                    for k in successors:
                        if player_color == "black":
                            if successor.utility > k.utility:
                                posToInsert = count
                                inserted = True
                                break
                        else:
                            if successor.utility < k.utility:
                                posToInsert = count
                                inserted = True
                                break
                        count += 1
                    if not inserted:
                        successors.append(successor)
                    else:
                        successors.insert(count, successor )

        return successors
