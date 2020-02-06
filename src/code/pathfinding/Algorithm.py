import math

from src.Settings import *
from src.code.environment.Map import Square
from src.code.math.vec2 import vec2


class Node(Square):
    def __init__(self, obstacles: [Square], parent=None, position=None):
        super().__init__(position, None, obstacles)
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.parent) + hash(self.position)


class AStar:
    def __init__(self, obstacles: [Square]):
        self.obstacles = obstacles
        self.closed = []
        self.open = []

        self.children = []  # AKA neighbours
        self.adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                         vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

    def update(self, obstacles: [Square]):
        self.obstacles = obstacles
        self.closed.clear()
        self.open.clear()
        self.children.clear()

    def getPath(self, start: vec2, end: vec2):
        startNode = Node(self.obstacles, None, start)
        endNode = Node(self.obstacles, None, end)

        self.closed.clear()
        self.open.clear()
        self.open.append(startNode)

        path = []

        currentNode = None

        # iterate until end is located
        while self.open:
            currentNode = self.open[0]
            currentIndex = 0

            for index, node in enumerate(self.open):
                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            self.open.pop(currentIndex)
            self.closed.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            neighbours = []
            for direction in self.adjacent:
                nodePos = currentNode.position + direction * TILE_SIZE
                node = Node(self.obstacles, currentNode, nodePos)

                if not node.walkable:
                    continue

                if node not in self.children and node not in self.closed:
                    neighbours.append(node)  # for current
                    self.children.append(node)  # for total

            for neighbour in neighbours:
                neighbourCost = currentNode.g + self.getCost(neighbour.position, startNode.position)

                for openNode in self.open:
                    if openNode.position == neighbour.position and neighbourCost > openNode.g:
                        continue

                neighbour.g = neighbourCost  # distance of neighbour and current
                neighbour.h = self.heuristic(neighbour.position, endNode.position)  # dist neigbour to end
                neighbour.f = neighbour.g + neighbour.h

                self.open.append(neighbour)

        # if computation is completed, traverse list (todo: heap)
        if currentNode:
            while currentNode:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1]

    #  Diagonal Manhattan
    def heuristic(self, node1, node2):
        dx = abs(node1.x - node2.x)
        dy = abs(node1.y - node2.y)
        d = 10
        d2 = 14
        return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy)

    def getCost(self, node1: vec2, node2: vec2):
        if (node2 - node1).normalized.length == 1:
            print("Horizontal")
            return 1  # horizontal cost
        else:
            print("Diagonal")
            return math.sqrt(2)  # diagonal cost
