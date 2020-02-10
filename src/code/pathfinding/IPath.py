from src.Settings import *
import math
import abc


class IPath(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self.graph = {}
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
        return (D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)) * 10

    @staticmethod
    def getCost(node1: vec2, node2: vec2):
        distance = int(node1.distance(node2))
        if distance == SETTINGS.TILE_HEIGHT:
            return 10  # horizontal/vertical cost
        else:
            return 14  # diagonal cost
