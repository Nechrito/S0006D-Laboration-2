import time

from src.Settings import SETTINGS
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate
from src.code.pathfinding.Node import Node
from src.code.pathfinding.IPath import IPath


class BreadthFirst(IPath):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.timerStart = time.time()
        self.timeElapsed = None

    def getPath(self, start: vec2, end: vec2):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = SETTINGS.getNode(start)
        self.queue = []
        self.queue.append(startNode)

        pathDict = {startNode: False}

        while True:
            if len(self.queue) == 0:
                return None

            currentNode = self.queue.pop(0)
            self.childNodes.append(currentNode)

            if currentNode.position == end:
                break

            for childPos in currentNode.neighbours:
                neighbour = SETTINGS.getNode(childPos)
                neighbour.parent = currentNode

                if neighbour.isWalkable and neighbour not in pathDict:
                    self.queue.append(neighbour)
                    pathDict[neighbour] = currentNode.position - neighbour.position

        path = self.backTrace(currentNode)

        self.timeElapsed = time.time() - self.timerStart
        print("[bfs] Time elapsed: " + str( truncate(self.timeElapsed * 1000)) + "ms")

        return path
