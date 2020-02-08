import math
import heapq

from src.Settings import *
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def push(self, data):
        heapq.heappush(self.queue, data)  # todo: (node, cost/weight)

    def pop(self):
        return heapq.heappop(self.queue)


class Node(Tile):
    def __init__(self, parent=None, position=None):
        super().__init__(position)
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.parent) + hash(self.position)


class AStar:
    def __init__(self, ):
        self.closed = []
        self.children = []
        self.adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                         vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

    def getPath(self, start: vec2, end: vec2):

        startNode = Node(None, start)
        endNode = Node(None, end)

        self.closed = []
        self.open = []
        self.open.append(startNode)

        self.children = []

        result = []
        currentNode = None

        # iterate until end is located
        while self.open:
            currentNode = self.open[0]
            currentIndex = 0

            for index, node in enumerate(self.open):
                if node.f == currentNode.f:
                    node.h += node.position.break_tie(startNode.position, endNode.position)

                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            self.open.pop(currentIndex)
            self.closed.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            if (currentNode.position.X + currentNode.position.Y) % 2 == 0:
                self.adjacent.reverse()

            neighbours = []
            for direction in self.adjacent:
                nodePos = currentNode.position + vec2(direction.X * SETTINGS.TILE_WIDTH, direction.Y * SETTINGS.TILE_HEIGHT)
                node = Node(currentNode, nodePos)

                if not node.isWalkable or not currentNode.isWalkable:
                    continue

                if node not in self.children:
                    neighbours.append(node)  # for current
                    self.children.append(node)  # for total

            for neighbour in neighbours:

                neighbourCost = currentNode.g + self.getCost(neighbour, currentNode)

                for openNode in self.open:
                    if openNode.position == neighbour.position and neighbourCost > openNode.g:
                        continue

                neighbour.g = neighbourCost  # distance of neighbour and current
                neighbour.h = self.heuristic(neighbour.position, endNode.position) # dist neigbour to end
                neighbour.f = neighbour.g + neighbour.h

                self.open.append(neighbour)

        # if computation is completed, traverse list (todo: heap)
        if currentNode:
            while currentNode:
                result.append(currentNode)
                currentNode = currentNode.parent
            return result[::-1]

    #  Diagonal Manhattan
    def heuristic(self, node1, node2):
        dx = abs(node1.X - node2.X)
        dy = abs(node1.Y - node2.Y)

        D = 1
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def getCost(self, node1, node2):

        dx = abs(node1.position.X - node2.position.X)
        dy = abs(node1.position.Y - node2.position.Y)
        center = vec2(dx, dy)
        distance = round(center.length)

        if distance == SETTINGS.TILE_HEIGHT:
            return 1.0  # horizontal/vertical cost
        else:
            return math.sqrt(2.0)  # diagonal cost
