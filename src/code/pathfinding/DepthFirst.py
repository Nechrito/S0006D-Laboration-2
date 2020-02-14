import time
from copy import copy

from src.Settings import SETTINGS
from src.code.math.cMath import truncate
from src.code.pathfinding.Node import Node
from src.code.pathfinding.IPath import IPath


class DepthFirst(IPath):

    def __init__(self):
        super().__init__()
        self.queue = []
        self.timerStart = time.time()
        self.timeElapsed = None

    def getPath(self, start, end):

        self.timerStart = time.time()
        self.timeElapsed = None

        #  might get back to same node, thus we use a set of booleans for visited nodes
        for i in range(50):
            result = self.iterate(start, end, i)
            if result is not None:
                return result

    def iterate(self, start, end, i):
        startNode = copy(SETTINGS.getNode(start))
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

            temp = []
            for childPos in currentNode.neighbours:
                neighbour = SETTINGS.getNode(childPos)

                if neighbour.isWalkable and neighbour not in pathDict:
                    neighbour.parent = currentNode.parent
                    temp.append(neighbour)
                    pathDict[neighbour] = currentNode.position - neighbour.position

            self.queue.extend(temp)

        path = self.backTrace(currentNode)

        self.timeElapsed = time.time() - self.timerStart
        print("[dfs] Time elapsed: " + str( truncate(self.timeElapsed * 1000)) + "ms | Path Length: " + str(len(path)))

        return path