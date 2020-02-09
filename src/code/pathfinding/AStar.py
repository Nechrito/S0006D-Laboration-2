import time

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.Parent import Parent


class AStar(Parent):

    def __init__(self):
        super().__init__()
        self.timerStart = None
        self.timeElapsed = None
        self.searchArea = []
        self.closed = []
        self.open = []

    def getPath(self, start: vec2, end: vec2):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = Node(None, start, True)
        endNode = Node(None, end, False)

        self.closed = []
        self.open = []
        self.open.append(startNode)
        self.searchArea = []

        result = []
        currentNode = None

        # iterate until end is located
        while self.open:
            currentNode = self.open[0]
            currentIndex = 0

            for index, node in enumerate(self.open):
                #if node.f == currentNode.f:
                    #node.h += node.position.break_tie(startNode.position, endNode.position)

                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            self.open.pop(currentIndex)
            self.closed.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            for pos in currentNode.neighbours:
                neighbour = Node(currentNode, pos, True)

                if not neighbour.isWalkable or neighbour in self.searchArea:
                    continue

                self.searchArea.append(neighbour)

                neighbour.g = currentNode.g + self.getCost(neighbour.position, currentNode.position)  # distance of neighbour and current
                neighbour.h = self.heuristic(neighbour.position, endNode.position)  # dist neigbour to end
                neighbour.f = neighbour.g + neighbour.h

                for openNode in self.open:
                    if openNode.position == neighbour.position and neighbour.g > openNode.g:
                        continue

                # print("g: " + str(neighbour.g) + " h: " + str(neighbour.h))
                self.open.append(neighbour)

        # if computation is completed, traverse list (todo: heap)
        if currentNode:
            while currentNode:
                result.append(currentNode)
                currentNode = currentNode.parent

            self.timeElapsed = time.time() - self.timerStart
            print("Time elapsed: " + str(self.timeElapsed))
            return result[::-1]

