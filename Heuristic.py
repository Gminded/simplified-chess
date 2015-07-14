from ChessBoard import DEFEAT

class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, table):
        #retrieve the utility value if it was already computed
        cachedValue = table.lookup(node.board)
        if cachedValue != None:
            node.SetUtility(cachedValue) #utility
            return cachedValue

        #weights
        winWeigth = 10000
        endangeredPawnsWeight = 20
        minDistanceWeight = 20
        avgDistanceWeight = 15
        enpassantWeight = 20
        pawnWeight = 20
        blockedPawnsWeight = 5
        movesWeight = 1
        clearSightWeight = 50

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
        playerAvgDistance = 0
        adversaryAvgDistance = 0
        playerPawnsEndangered = 0
        playerPawnsClearSight = 0
        adversaryPawnsClearSight = 0
        adversaryPawnsEndangered = 0

        #board state
        board = node.GetState()
        oldboard = node.GetOldState()

        #my pieces
        playerColor = "black"
        adversaryColor = "white"
        playerPawns = node.board.blackPawns
        adversaryPawns = node.board.whitePawns

        #checking victory state
        if node.board.TerminalTest(playerColor) == DEFEAT:
            score = -1
        elif node.board.TerminalTest(adversaryColor) == DEFEAT:
            score = 1

        #checking number of legal moves
        playerMoves = node.LegalMoves(playerColor)
        adversaryMoves = node.LegalMoves(adversaryMoves)

        direction = 1
        #Two loops for counting player and adversary stuff
        for pawn in playerPawns:
            pawnRow = pawn[0]
            pawnCol = pawn[1]

            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                playerEnpassant += 1

            #counting number of pawns which can be captured during the next turn (and the one after)
            if pawnRow + direction < 6 and pawnCol + 1 < 8 and node.board.state[ pawnRow + direction ][ pawnCol + 1 ] != "e":
                playerPawnsEndangered += 1
            if pawnRow + direction < 6 and pawnCol - 1 >= 0 and node.board.state[ pawnRow + direction ][ pawnCol - 1 ] != "e":
                playerPawnsEndangered += 1
            if pawnRow + direction*2 < 6 and pawnCol + 1 < 8 and node.board.state[ pawnRow + direction*2 ][ pawnCol + 1 ] != "e":
                playerPawnsEndangered += 1
            if pawnRow + direction*2 < 6 and pawnCol - 1 >= 0 and node.board.state[ pawnRow + direction*2 ][ pawnCol - 1 ] != "e":
                playerPawnsEndangered += 1

            #counting number of blocked pawns
            if pawnRow + direction < 8 and node.board.state[ pawnRow + direction ][ pawnCol ] != "e":
                blockedPlayerPawns+= 1

            #number of pawns which have a clear sight to the end of the board
            for pos in range(pawnRow + direction, 8):
                if node.board.state[ pos ][pawnCol] != "e":
                    if pawnCol + 1 < 8 and node.board.state[ pos ][pawnCol +1] != "e":
                        if pawnCol -1 >= 0 and node.board.state[ pos ][pawnCol -1] != "e":
                            break
                else:
                    if pos == 7:
                        playerPawnsClearSight +=1

            #counting minDistance from the other end of the board
            distance = 7 - pawnRow
            playerAvgDistance += distance
            if distance < playerMinDistance:
                playerMinDistance = distance
        if len(playerPawns):
            playerAvgDistance = float(playerAvgDistance) / len(playerPawns)
        else:
            playerAvgDistance = 10

        direction = -1
        for pawn in adversaryPawns:
            pawnRow = pawn[0]
            pawnCol = pawn[1]

            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                adversaryEnpassant += 1

            #counting number of pawns which can be captured during the next turn (and the one after)
            if pawnRow + direction >= 0 and pawnCol + 1 < 8 and node.board.state[ pawnRow + direction ][ pawnCol + 1 ] != "e":
                adversaryPawnsEndangered += 1
            if pawnRow + direction >= 0 and pawnCol - 1 >= 0 and node.board.state[ pawnRow + direction ][ pawnCol - 1 ] != "e":
                adversaryPawnsEndangered += 1
            if pawnRow + direction*2 >= 0 and pawnCol + 1 < 8 and node.board.state[ pawnRow + direction*2 ][ pawnCol + 1 ] != "e":
                adversaryPawnsEndangered += 1
            if pawnRow + direction*2 >= 0 and pawnCol - 1 >= 0 and node.board.state[ pawnRow + direction*2 ][ pawnCol - 1 ] != "e":
                adversaryPawnsEndangered += 1

            #counting number of blocked pawns
            if pawnRow + direction >= 0 and node.board.state[ pawnRow + direction ][ pawnCol ] != "e":
                blockedAdversaryPawns+= 1

            #number of pawns which have a clear sight to the end of the board
            for pos in range(pawnRow + direction, direction, direction):
                if node.board.state[ pos ][pawnCol] != "e":
                    if pawnCol + 1 < 8 and node.board.state[ pos ][pawnCol +1] != "e":
                        if pawnCol -1 >= 0 and node.board.state[ pos ][pawnCol -1] != "e":
                            break
                else:
                    if pos == 7:
                        adversaryPawnsClearSight +=1

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
        node.SetUtility( winWeigth*( score ) + minDistanceWeight*( adversaryMinDistance -  playerMinDistance ) +
                         int( avgDistanceWeight*(adversaryAvgDistance - playerAvgDistance) ) +
                         enpassantWeight*( playerEnpassant - adversaryEnpassant ) +
                         pawnWeight*( len(playerPawns) - len(adversaryPawns) ) +
                         blockedPawnsWeight*( blockedAdversaryPawns - blockedPlayerPawns ) +
                         movesWeight*( playerMoves - adversaryMoves ) - endangeredPawnsWeight*(  adversaryPawnsEndangered - playerPawnsEndangered ) +
                         clearSightWeight*( playerPawnsClearSight - adversaryPawnsClearSight ))