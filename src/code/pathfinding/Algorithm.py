import heapq  # <-- https://docs.python.org/3/library/heapq.html

from src.Settings import TILE_SIZE
from src.code.math.vec2 import vec2


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class AStar:
    def __init__(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles
        self.closed = []
        self.open = []
        self.path = []
        self.neighbours = []
        self.directions = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                           vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

    def getPath(self, start: vec2, end: vec2):
        # F = G + H
        #   G = self.cost(start, node)
        #   H = self.cost(node, end)
        self.closed.clear()
        self.open = []  # our heap for priority queue
        heapq.heappush(self.open, (start, 0))

        self.path = {start: None}
        self.costs = {start: 0}

        while self.open:  # <- python is stupid, this is the same as .empty()

            heap = heapq.heappop(self.open)  # smallest item in heap
            currentNode = heap[0]
            currentCost = heap[1]

            if currentNode == end:  # no need to search further
                break

            self.neighbours = []
            for direction in self.directions:
                self.neighbours.append(currentNode + direction)

            for neighbour in self.neighbours:

                if neighbour in self.closed:
                    continue

                neighbourCost = self.costs[currentCost] + self.getCost(currentNode, neighbour)

                if neighbourCost < self.costs[currentCost]:
                    self.costs[neighbour] = neighbourCost
                    prio = neighbourCost + self.heuristic(end, neighbour)
                    heapq.heappush(self.open, (neighbour, prio))
                    self.path[neighbour] = currentNode - neighbour
                    print("added")

        return self.path

    def update(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles

    def heuristic(self, node1, node2):
        return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10

    def getCost(self, node1: vec2, node2: vec2):
        distance = (node2 - node1)

        if distance.lengthSquared == 1:
            return 10  # horizontal cost
        else:
            return 14  # diagonal cost

    def isWalkable(self, node):
        for i in range(len(self.obstacles)):
            temp = self.grid[i]
            if temp.collidepoint(node):
                return False
        return True
