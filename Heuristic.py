from ChessBoard import DEFEAT
from ZobristHash import ZobristHash

class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, table):
        #retrieve the utility value if it was already computed
        cachedValue = table.lookup(node.board)
        if cachedValue != None:
            print "cached"
            node.SetUtility(cachedValue) #utility
            return

        #weights
        winWeigth = 1000000
        minDistanceWeight = 10
        avgDistanceWeight = 10
        enpassantWeight = 30
        pawnWeight = 20
        blockedPawnsWeight = 5
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
        playerAvgDistance = 0
        adversaryAvgDistance = 0

        adversaryColor = None

        #board state
        board = node.GetState()
        oldboard = node.GetOldState()

        #my pieces

        direction = 1
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

        #Two loops for counting player and adversary stuff
        for pawn in playerPawns:
            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                playerEnpassant += 1

            #counting number of blocked pawns
            elif node.board.state[ pawn[0] + direction ][ pawn[1] ] != "e":
                blockedPlayerPawns+= 1

            #counting minDistance from the other end of the board
            distance = 7 - pawn[0]
            playerAvgDistance += distance
            if distance < playerMinDistance:
                playerMinDistance = distance
        playerAvgDistance = float(playerAvgDistance) / len(playerPawns)

        for pawn in adversaryPawns:
            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                adversaryEnpassant += 1

            #counting number of blocked pawns
            elif node.board.state[ pawn[0] + direction ][ pawn[1] ] != "e":
                blockedAdversaryPawns+= 1

            #counting minDistance from the other end of the board
            distance = pawn[0]
            adversaryAvgDistance += distance
            if distance < adversaryMinDistance:
                adversaryMinDistance = distance
        adversaryAvgDistance = float(adversaryAvgDistance) / len(adversaryPawns)

        #computing value
        node.SetUtility( winWeigth*( score ) + minDistanceWeight*( adversaryMinDistance -  playerMinDistance ) +
                         avgDistanceWeight*(adversaryAvgDistance - playerAvgDistance) +
                         enpassantWeight*( playerEnpassant - adversaryEnpassant ) +
                         pawnWeight*( len(playerPawns) - len(adversaryPawns) ) +
                         blockedPawnsWeight*( blockedAdversaryPawns - blockedPlayerPawns ) +
                         movesWeight*( playerMoves - adversaryMoves ) )
        table.insertUtility(node.board, node.utility)
