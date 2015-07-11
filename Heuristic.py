import Node
import random

class Heuristic:

    @staticmethod
    def HeuristicFunction( node):
            random.seed(None)
            node.utility = random.randint(1,100)