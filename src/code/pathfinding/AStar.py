import time

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.IPath import IPath


class AStar(IPath):

    def __init__(self):
        super().__init__()

    def getPath(self, start: vec2, end: vec2):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = Node(None, start, True)
        endNode = Node(None, end, False)

        closedList = []
        openList = [startNode]

        result = []
        currentNode = None

        # iterate until end is located
        while openList:
            currentNode = openList[0]
            currentIndex = 0

            for index, node in enumerate(openList):
                if node.f == currentNode.f:
                    node.h += node.position.break_tie(startNode.position, endNode.position)

                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            openList.pop(currentIndex)
            closedList.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            for pos in currentNode.neighbours:
                neighbour = Node(currentNode, pos, True)

                if not neighbour.isWalkable or neighbour in closedList:
                    continue

                if neighbour not in self.childNodes:
                    self.childNodes.append(neighbour)

                cost = currentNode.g + self.getCost(neighbour.position, currentNode.position)

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
            while currentNode:
                result.append(currentNode)
                currentNode = currentNode.parent

            self.timeElapsed = time.time() - self.timerStart
            print("Time elapsed: " + str(self.timeElapsed))
            return result[::-1]

