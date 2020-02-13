from src.code.environment.Tile import Tile


class Node(Tile):
    def __init__(self, parent=None, position=None, loadNeighbours=None):
        super().__init__(position)
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        if loadNeighbours:
            self.addNeighbour()
            self.isWalkable = self.validate()

    def __lt__(self, other):
        return self.f < other.f

