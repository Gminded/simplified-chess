from ChessBoard import DEFEAT
from ChessBoard import WON

class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, table, depth, color):
        #retrieve the utility value if it was already computed
        cachedValue = table.lookup(node.board)
        if cachedValue != None and cachedValue[1] >= depth:
            node.SetUtility(cachedValue[0]) #utility
            return cachedValue

        #weights
        minDistanceWeight = 5
        avgDistanceWeight = 5
        pawnWeight = 40
        movesWeight = 1
        distanceFromKingWeigth = -5

        playerMinDistance = 10
        adversaryMinDistance = 10
        playerAvgDistance = 0
        adversaryAvgDistance = 0
        playerAvgDistanceFromKing = 0
        adversaryAvgDistanceFromKing = 0

        #my pieces
        playerColor = "b"
        adversaryColor = "w"
        playerPawns = node.board.blackPawns
        adversaryPawns = node.board.whitePawns

        #checking number of legal moves
        playerMoves = node.LegalMoves(playerColor)
        adversaryMoves = node.LegalMoves(adversaryColor)

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
            pawnCol = pawn[1]

            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                adversaryEnpassant += 1

            #distance from adv King
            distance = abs( (node.board.whiteKing[0] +node.board.whiteKing[1] ) - ( pawnRow + pawnCol))
            adversaryAvgDistanceFromKing += distance

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
                    if pawnCol + 1 < 8:
                        if node.board.state[ pos ][pawnCol +1] != "e":
                            break
                    if pawnCol -1 >= 0:
                        if node.board.state[ pos ][pawnCol -1] != "e":
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

        if len(adversaryPawns) != 0:
            adversaryAvgDistanceFromKing = adversaryAvgDistanceFromKing / len(adversaryPawns)
        else:
            adversaryAvgDistanceFromKing = 0

        #computing value
        node.SetUtility(minDistanceWeight*( adversaryMinDistance -  playerMinDistance ) +
                         int( avgDistanceWeight*(adversaryAvgDistance - playerAvgDistance) ) +
                         pawnWeight*( len(playerPawns) - len(adversaryPawns) ) +
                         movesWeight*( playerMoves - adversaryMoves ) +
                         distanceFromKingWeigth*(int( playerAvgDistanceFromKing ) ) )
