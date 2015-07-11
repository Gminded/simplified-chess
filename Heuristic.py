from Node import Node
import random

class Heuristic:
    def HeuristicFunction(self, node):
            random.seed(None)
            return random.randint(1,100)