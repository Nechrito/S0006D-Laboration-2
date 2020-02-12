
from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar
from src.code.pathfinding.BreadthFirst import BreadthFirst
from src.code.pathfinding.DepthFirst import DepthFirst
from src.enums.PathType import PathType


def getFullPath(waypoints, startIndex: int = 0):
    distance = 0
    for i in range(startIndex, len(waypoints) - 1):
        distance += waypoints[i].position.distance(waypoints[i + 1].position)
    return distance


class PathManager:

    def __init__(self, pathType: PathType = 0):
        self.updateTime = 0
        if pathType == 0:
            self.algorithm = AStar()
        elif pathType == 1:
            self.algorithm = DepthFirst()
        elif pathType == 2:
            self.algorithm = BreadthFirst()

    def requestPathCached(self, waypoints, owner, end: vec2):
        if len(waypoints) >= 2:
            return waypoints
        return self.algorithm.getPath(owner.position, end)

    def requestPath(self, start: vec2, end: vec2):
        return self.algorithm.getPath(start, end)

    def requestChildren(self):
        return self.algorithm.childNodes

    def cutPath(self, owner, waypoints):
        indices = []
        for node in waypoints:
            if node.position.distance(owner.position) > owner.radius:
                indices.append(node)

        return indices
