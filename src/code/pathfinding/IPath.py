import math
import abc

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node


class IPath(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self.childNodes = []
        self.timerStart = None
        self.timeElapsed = None

    @abc.abstractmethod
    def getPath(self, start: vec2, end: vec2):
        pass

    #  Diagonal Manhattan
    @staticmethod
    def heuristic(node1, node2):
        dx = abs(node1.X - node2.X)
        dy = abs(node1.Y - node2.Y)

        D = 1
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    @staticmethod
    def getCost(node1: Node, node2: Node):
        if int(node2.position.X - node1.position.X) == 0 or int(node2.position.Y - node1.position.Y) == 0:
            cost = 1  # horizontal/vertical cost
        else:
            cost = math.sqrt(2)  # diagonal cost
        return node1.g + cost

    @staticmethod
    def backTrace(node):
        path = [node]
        while node.parent:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

    def backTraceBi(self, node1, node2):
        path1 = self.backTrace(node1)
        path2 = self.backTrace(node2)
        path2.reverse()
        return path1 + path2

