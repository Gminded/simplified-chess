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


    #return successor nodes
    def Actions(self, player_color, maxPlayer, threaded=None, threadIndex=-1, threadTotal=-1):
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
                Heuristic.ShannonHeuristic(successor, player_color)

                #ordering (descending)
                count = 0
                inserted = False
                if not successors:
                    successors.append(successor)
                else:
                    for k in successors:
                        if maxPlayer:
                            if successor.utility > k.utility:
                                successors.insert(count, successor )
                                inserted = True
                                break
                        else:
                            if successor.utility < k.utility:
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
