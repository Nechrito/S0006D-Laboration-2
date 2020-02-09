from src.Settings import *
import math


class Parent:

    #  Diagonal Manhattan
    def heuristic(self, node1, node2):
        dx = abs(node1.X - node2.X)
        dy = abs(node1.Y - node2.Y)

        D = 1
        D2 = math.sqrt(2)
        return (D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)) * 10

    def getCost(self, node1: vec2, node2: vec2):
        distance = int(node1.distance(node2))
        if distance == SETTINGS.TILE_HEIGHT:
            return 10  # horizontal/vertical cost
        else:
            return 14  # diagonal cost
