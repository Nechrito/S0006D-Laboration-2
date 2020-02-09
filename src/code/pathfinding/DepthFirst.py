import time

from src.code.pathfinding.Node import Node
from src.code.pathfinding.Parent import Parent


class DepthFirst(Parent):

    def __init__(self):
        super().__init__()
        self.timerStart = time.time()
        self.timeElapsed = None

    def getPath(self, start, end):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = Node(None, start)

