import heapq  # <-- https://docs.python.org/3/library/heapq.html

import pygame

from src.Settings import *
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

    def __hash__(self):
        return hash(self.parent) + hash(self.position)


class AStar:
    def __init__(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles
        self.closed = []
        self.open = []
        self.path = []
        self.neighbours = []
        self.adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                         vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

    def getPath(self, start: vec2, end: vec2):
        startNode = Node(None, start)
        endNode = Node(None, end)

        self.closed.clear()
        self.open.clear()
        self.open.append(startNode)

        self.path.clear()

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
                curent = currentNode
                while curent:
                    self.path.append(curent.position)
                    curent = curent.parent

                return self.path[::-1]

            for direction in self.adjacent:
                nodePos = currentNode.position + direction * TILE_SIZE

                if not self.isWalkable(nodePos):
                    continue

                node = Node(currentNode, nodePos)

                if node not in self.neighbours and node not in self.closed:
                    self.neighbours.append(node)

            for neighbour in self.neighbours:

                neighbour.g = currentNode.g + self.getCost(neighbour.position, currentNode.position) + TILE_SIZE  # distance of neighbour and current
                neighbour.h = self.heuristic(neighbour.position, endNode.position)  # dist neigbour to end
                neighbour.f = neighbour.g + neighbour.h

                for openNode in self.open:
                    if neighbour.position == openNode.position and neighbour.g >= openNode.g:
                        continue

                self.open.append(neighbour)

    def update(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles

    def heuristic(self, node1, node2):
        return (abs(node1.x - node2.x) ** 2) + (abs(node1.y - node2.y) ** 2)
        #return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10

    def getCost(self, node1: vec2, node2: vec2):
        if (node2 - node1).length == 1:
            return 10  # horizontal cost
        else:
            return 14  # diagonal cost

    def isWalkable(self, node):

        bb = TILE_SIZE + TILE_SIZE / 2
        if node.x > SCREEN_WIDTH - bb or node.x < bb or node.y > SCREEN_HEIGHT - bb or node.y < bb:
            return False

        for obstacle in self.obstacles:
            rect = pygame.Rect(obstacle[0], obstacle[1], TILE_SIZE, TILE_SIZE)
            if rect.collidepoint((node.x, node.y)):
                return False
        return True
