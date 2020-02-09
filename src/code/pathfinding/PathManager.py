

from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar
from src.code.pathfinding.BreadthFirst import BreadthFirst
from src.code.pathfinding.DepthFirst import DepthFirst


class PathManager:
    def __init__(self):
        self.astar = AStar()
        self.dfs = DepthFirst()
        self.bfs = BreadthFirst()

    def requestPath(self, start: vec2, end: vec2):
        return self.astar.getPath(start, end)  # todo: cut path if possible

    def requestNeighbours(self):
        return self.astar.searchArea
