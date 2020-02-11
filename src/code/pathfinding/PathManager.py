import time
from collections import defaultdict

from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar


class PathManager:

    def __init__(self, algorithm = None):
        self.updateTime = 0
        self.path = []
        if algorithm:
            self.algorithm = algorithm
        else:
            self.algorithm = AStar()

    def requestPathCached(self, owner, end: vec2):
        if len(self.path) >= 1:
            return self.path
        self.path = self.algorithm.getPath(owner.position, end)
        return self.path

    def requestPath(self, start: vec2, end: vec2):
        return self.algorithm.getPath(start, end)

    def requestChildren(self):
        return self.algorithm.childNodes

    def update(self, owner):
        self.path = self.cutPath(owner)

    def cutPath(self, owner):
        indices = []
        for node in self.path:
            if node.position.distance(owner.position) > owner.radius:
                indices.append(node)
        return indices


