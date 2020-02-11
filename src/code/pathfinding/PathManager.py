from typing import List

from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar
from src.code.pathfinding.Node import Node


def getFullPath(waypoints, startIndex: int = 0):
    distance = 0
    for i in range(startIndex, len(waypoints) - 1):
        distance += waypoints[i].position.distance(waypoints[i + 1].position)
    return distance


class PathManager:

    path: List[Node]

    def __init__(self, algorithm = None):
        self.updateTime = 0
        self.path = []
        if algorithm:
            self.algorithm = algorithm
        else:
            self.algorithm = AStar()

    def requestPathCached(self, owner, end: vec2):
        if len(self.path) >= 2:
            return self.path
        self.path = self.algorithm.getPath(owner.position, end)
        return self.path

    def requestPath(self, start: vec2, end: vec2):
        return self.algorithm.getPath(start, end)

    def requestChildren(self):
        return self.algorithm.childNodes

    def cutPath(self, owner):
        indices = []
        for node in self.path:
            if node.position.distance(owner.position) > owner.radius:
                indices.append(node)

        self.path = indices


