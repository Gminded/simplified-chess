#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
import threading
from Heuristic import Heuristic

class ChessAI:
    def __init__(self, name, color):
        # print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.alpha = -1000
        self.beta = 1000
        self.lock = threading.Lock()


    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def GetMove(self, currentNode, depth,threaded=False, threadTotal=-1):
        actions = currentNode.Actions("black")
        bestMoveTuple = None

        #use multithreading?
        if not threaded:
            bestMoveUtility = self.AlphaBetaSearch(currentNode=currentNode, depth=depth, actions=actions)
        else:
            threads = [None] * threadTotal
            ret_values = [-1000] * threadTotal
            for i in range(threadTotal):
                threads[i] = threading.Thread( None, target=self.storeAlphaBetaThreaded, name=None, args=(ret_values, i, currentNode, depth, threadTotal), kwargs={})
                threads[i].start()
  #          for i in range(threadTotal):
 #               threads[i].join()
            bestMoveUtility = max(ret_values)

        #get the best move tuple
        for i in actions:
            if i.utility == bestMoveUtility:
                bestMoveTuple = i.GetMoveTuple()
                break
        return bestMoveTuple

    def AlphaBetaSearch(self, alpha=-1000, beta=1000, currentNode=None, maxPlayer=True, depth=0, actions=None):
        if maxPlayer:
            playerColor = "black"
        else:
           playerColor = "white"

        #terminal test1
        if depth == 0:
            Heuristic.ShannonHeuristic(currentNode, playerColor)
            return currentNode.utility

        if actions == None and maxPlayer:
            actions = currentNode.Actions("black")
        else:
            actions = currentNode.Actions("white")

        #terminal test2
        if len(actions) == 0:
            Heuristic.ShannonHeuristic(currentNode, playerColor)
            return currentNode.utility

        if maxPlayer:
            v = -1000
            for node in actions:
                v = max(v, self.AlphaBetaSearch( alpha, beta, node, False, depth-1 ) )
                if v >= beta:
                    return beta
                if v > alpha:
                    alpha = v
            return alpha
        else:
            v = 1000
            for node in actions:
                v = min(v, self.AlphaBetaSearch( alpha, beta, node, True, depth-1 ) )
                if v <= alpha:
                    return alpha
                if v < beta:
                    beta = v
            return beta

    def storeAlphaBetaThreaded(self, data, threadIndex, currentNode, depth, threadTotal):
        data[threadIndex] = self.AlphaBetaSearchThreaded( currentNode=currentNode, depth=depth, threaded=True, threadTotal=threadTotal, threadIndex=threadIndex)

    def AlphaBetaSearchThreaded(self, currentNode=None, maxPlayer=True, depth=0, threaded=True, threadTotal=1, threadIndex=-1):
        if maxPlayer:
            actions = currentNode.Actions("black", threaded=True, threadIndex=threadIndex,threadTotal=threadTotal)
        else:
            actions = currentNode.Actions("white", threaded=True, threadIndex=threadIndex,threadTotal=threadTotal)

        #terminal test
        if depth == 0 or len(actions) == 0:
            Heuristic.HeuristicFunction(currentNode)
            return currentNode.utility

        if maxPlayer:
            v = -1000
            for node in actions:
                v = max(v, self.AlphaBetaSearchThreaded( node, False, depth-1, True, threadTotal, threadIndex ) )

                #CS START
                self.lock.acquire()
                if v >= self.beta:
                    return self.beta
                if v > self.alpha:
                    self.alpha = v
                self.lock.release()
                #CS END

            return self.alpha
        else:
            v = 1000
            for node in actions:
                v = min(v, self.AlphaBetaSearchThreaded( node, True, depth-1, True, threadTotal, threadIndex ) )

                #CS START
                self.lock.acquire()
                if v <= self.alpha:
                    return self.alpha
                if v < self.beta:
                    self.beta = v
                self.lock.release()
                #CS END

            return self.beta