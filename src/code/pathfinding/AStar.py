import time
from copy import copy

from src.Settings import SETTINGS
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate
from src.code.pathfinding.IPath import IPath
from src.enums.PathType import PathType


class AStar(IPath):

    def __init__(self):
        super().__init__()

    def getPath(self, start: vec2, end: vec2):
        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = SETTINGS.getNode(start)
        endNode = SETTINGS.getNode(end)

        closedList = []
        openList = [startNode]

        currentNode = None

        # iterate until end is located
        while openList:
            currentNode = openList[0]
            currentIndex = 0

            for index, node in enumerate(openList):
                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            openList.pop(currentIndex)
            closedList.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            for pos in currentNode.neighbours:
                neighbour = SETTINGS.getNode(pos)
                if not neighbour.isWalkable or neighbour in closedList:
                    continue

                neighbour.parent = currentNode

                #print(str(neighbour))

                if neighbour not in self.childNodes:
                    self.childNodes.append(neighbour)

                cost = currentNode.g + self.getCost(neighbour, currentNode)

                if neighbour in openList:
                    if neighbour.g > cost:
                        neighbour.g = cost
                else:
                    neighbour.g = cost
                    openList.append(neighbour)

                neighbour.h = self.heuristic(neighbour.position, endNode.position)
                neighbour.f = neighbour.g + neighbour.h

                # print("g: " + str(neighbour.g) + " h: " + str(neighbour.h))

        # if computation is completed, traverse list (todo: heap)
        if currentNode:
            path = []
            while currentNode:
                path.append(currentNode)
                currentNode = currentNode.parent

            self.timeElapsed = (time.time() - self.timerStart) * 1000
            self.computeAverage(self.timeElapsed, PathType.AStar)
            print("[A*] Elapsed: " + str( truncate(self.timeElapsed)) +
                  "ms (Avg. " + str( truncate(self.getAverage(PathType.AStar)) ) +
                  "ms) | Path Length: " + str(len(path)))

            return path[::-1]

