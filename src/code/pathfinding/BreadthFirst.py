import time
from collections import deque

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.IPath import IPath
from src.Settings import *


class BreadthFirst(IPath):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.timerStart = time.time()
        self.timeElapsed = None

    def getPath(self, start: vec2, end: vec2):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = Node(None, start, True)
        self.queue = []
        self.queue.append(startNode)

        path = {startNode: False}

        while self.queue:
            currentNode = self.queue.pop()

            for childPos in currentNode.neighbours:
                neighbour = Node(currentNode, childPos, True)

                if neighbour not in path:
                    self.queue.append(neighbour)
                    path[neighbour] = currentNode.position - neighbour.position

        result = []
        for node, dir in path.items():
            if dir:
                result.append(node)

        self.timeElapsed = time.time() - self.timerStart
        print("Time elapsed: " + str(self.timeElapsed))

        return result
