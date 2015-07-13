from ChessBoard import DEFEAT
from ZobristHash import ZobristHash

class Heuristic:

    @staticmethod
    def ShannonHeuristic(node, playerColor, table={}):
        #retrieve the utility value if it was already computed
        cachedValue = table.lookup(node.board)
        if cachedValue != None:
            node.SetUtility(cachedValue[0]) #utility
            return

        #weights
        winWeigth = 200
        distanceWeight = 80
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

        adversaryColor = None

        #board state
        board = node.GetState()
        oldboard = node.GetOldState()

        #my pieces
        if playerColor == "black":
            direction = 1
            otherEnd = -7
            adversaryColor = "white"
            playerPawns = node.board.blackPawns
            adversaryPawns = node.board.whitePawns
        else:
            direction = -1
            otherEnd = 0
            adversaryColor = "black"
            playerPawns = node.board.whitePawns
            adversaryPawns = node.board.blackPawns

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
            if pawn[0] + direction > 7 or pawn[0] + direction < 0:
                blockedPlayerPawns+= 1
            elif node.board.state[ pawn[0] + direction ][ pawn[1] ] != "e":
                blockedPlayerPawns+= 1

            #counting minDistance from the other end of the board
            distance = otherEnd + pawn[0]
            if distance < playerMinDistance:
                playerMinDistance = distance

        for pawn in adversaryPawns:
            #Checking enpassant
            if node.board.IsEnpassantPawn(pawn):
                adversaryEnpassant += 1

            #counting number of blocked pawns
            if pawn[0] + direction > 7 or pawn[0] + direction < 0:
                blockedAdversaryPawns+= 1
            elif node.board.state[ pawn[0] + direction ][ pawn[1] ] != "e":
                blockedAdversaryPawns+= 1

            #counting minDistance from the other end of the board
            distance = otherEnd + pawn[0]
            if distance < playerMinDistance:
                playerMinDistance = distance

        #computing value
        node.SetUtility( winWeigth*( score ) + distanceWeight*( playerMinDistance - adversaryMinDistance ) +
                         enpassantWeight*( playerEnpassant - adversaryEnpassant ) +
                         pawnWeight*( len(playerPawns) - len(adversaryPawns) ) +
                         blockedPawnsWeight*( blockedAdversaryPawns - blockedPlayerPawns ) +
                         movesWeight*( playerMoves - adversaryMoves ) )
        table.insertUtility(node.board, node.utility)
