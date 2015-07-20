class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, table, depth, color):
        #retrieve the utility value if it was already computed
        cachedValue = table.lookup(node.board)
        if cachedValue != None and not cachedValue[0] is None:
            return cachedValue

        #weights
        minDistanceWeight = 5
        avgDistanceWeight = 5
        pawnWeight = 40
        movesWeight = 1
        distanceFromKingWeight = -5

        #Heuristic values
        score = 0
        playerMinDistance = 10
        adversaryMinDistance = 10
        playerAvgDistance = 0
        adversaryAvgDistance = 0
        playerAvgDistanceFromKing = 0
        adversaryAvgDistanceFromKing = 0

        #my pieces
        playerColor = node.board.BLACK
        adversaryColor = node.board.WHITE
        playerPawns = node.board.blackPawns
        adversaryPawns = node.board.whitePawns

        #checking number of legal moves
        playerMoves = len(node.board.getAllValidMoves(playerColor))
        adversaryMoves = len(node.board.getAllValidMoves(adversaryColor))

        direction = 1
        #Two loops for counting player and adversary stuff
        for pawn in playerPawns:
            pawnRow = pawn[0]
            pawnCol = pawn[1]

            #distance from adv King
            distance = abs( (node.board.blackKing[0] +node.board.blackKing[1] ) - ( pawnRow + pawnCol))
            playerAvgDistanceFromKing += distance

            #counting minDistance from the other end of the board
            distance = 7 - pawnRow
            playerAvgDistance += distance
            if distance < playerMinDistance:
                playerMinDistance = distance
        if len(playerPawns) != 0:
            playerAvgDistance = float(playerAvgDistance) / len(playerPawns)
        else:
            playerAvgDistance = 10

        if len(playerPawns) != 0:
            playerAvgDistanceFromKing = playerAvgDistanceFromKing / len(playerPawns)
        else:
            playerAvgDistanceFromKing = 0

        direction = -1
        for pawn in adversaryPawns:
            pawnRow = pawn[0]

            #counting minDistance from the other end of the board
            distance = pawnRow
            adversaryAvgDistance += distance
            if distance < adversaryMinDistance:
                adversaryMinDistance = distance
        if len(adversaryPawns) > 0:
            adversaryAvgDistance = float(adversaryAvgDistance) / len(adversaryPawns)
        else:
            adversaryAvgDistance = 10

        #computing value
        return (minDistanceWeight*( adversaryMinDistance -  playerMinDistance ) +
                         int( avgDistanceWeight*(adversaryAvgDistance - playerAvgDistance) ) +
                         pawnWeight*( len(playerPawns) - len(adversaryPawns) ) +
                         movesWeight*( playerMoves - adversaryMoves ) +
                         distanceFromKingWeight*(int( playerAvgDistanceFromKing ) ) )
