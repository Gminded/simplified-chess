class Heuristic:

    @staticmethod
    def HeuristicFunction(node):
        node.SetUtility(1)

    @staticmethod
    def ShannonHeuristic(node, playerColor):
        #weights
        winWeigth = 200
        distanceWeight = 50
        enpassantWeight = 5
        pawnWeight = 5
        blockedPawnsWeight = 2
        movesWeight = 1

        #Heuristic values
        playerEnpassant = 0
        adversaryEnpassant = 0
        score = 0
        playerPawns = []
        adversaryPawns = []
        playerMoves = 0
        adversaryMoves = 0
        blockedPlayerPawns = 0
        blockedAdversaryPawns = 0
        playerMinDistance = 10
        adversaryMinDistance = 10

        #board state
        board = node.GetState()
        oldboard = node.GetOldState()

        #my pieces
        if playerColor == "black":
            playerPawns = node.board.blackPawns
            adversaryPawns = node.board.whitePawns
        else:
            playerPawns = node.board.whitePawns
            adversaryPawns = node.board.blackPawns

        #Checking enpassant
        for pawn in playerPawns:
            if rules.IsEnpassantPawn(board, oldboard):
                playerEnpassant += 1
        for pawn in adversaryPawns:
            if rules.IsEnpassantPawn(oldboard, board):
                adversaryEnpassant += 1

        #Checking