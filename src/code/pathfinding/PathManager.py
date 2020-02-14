from src.Settings import SETTINGS
from src.code.math.Iterator import fori
from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar
from src.code.pathfinding.BreadthFirst import BreadthFirst
from src.code.pathfinding.DepthFirst import DepthFirst
from src.enums.PathType import PathType


def getFullPath(waypoints, startIndex: int = 0):
    distance = 0
    for i in range(startIndex, len(waypoints) - 1):
        startP = waypoints[i].position
        nextP = waypoints[i + 1].position
        distance += (nextP - startP).length
    return distance


class PathManager:

    def __init__(self, pathType: PathType = 0):
        self.updateTime = 0
        self.pathType = pathType

        if pathType == PathType.AStar:
            self.algorithm = AStar()
        elif pathType == PathType.DFS:
            self.algorithm = DepthFirst()
        elif pathType == PathType.BFS:
            self.algorithm = BreadthFirst()

    def requestPathCached(self, waypoints, start, end: vec2):
        if waypoints and len(waypoints) >= 2 and end == waypoints[-1]:
            return waypoints

        return self.requestPath(start, end)

    def requestPath(self, start: vec2, end: vec2):
        self.algorithm.childNodes = []
        path = self.algorithm.getPath(start, end)

        if not path or len(path) <= 2:
            return None

        found = False
        for p in path:
            if p.position == end:
                found = True
                break
        if not found:
            return None

        return path

    def requestChildren(self):
        return self.algorithm.childNodes

    def getAlgorithm(self):
        return self.algorithm

    def getPathType(self):
        return self.pathType

    def cutPath(self, owner, waypoints):
        indices = []
        for node in waypoints:
            if node.position.distance(owner.position) > owner.radius:
                indices.append(node)

        return indices
