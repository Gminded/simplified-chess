import Node
import random

class Heuristic:
    def HeuristicFunction(self, node):
            random.seed(None)
            node.utility = random.randint(1,100)