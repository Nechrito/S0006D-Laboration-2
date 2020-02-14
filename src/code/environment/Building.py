import random

from src.Settings import SETTINGS
from src.code.math.Vector import vec2


class Building:
    def __init__(self, position: vec2, name: str, description: str = None):
        self.position = position
        self.name = name
        self.description = description

        threshold = 8
        temp = vec2(self.position.X + random.randrange(-threshold, threshold), self.position.Y + random.randrange(-threshold, threshold / 2))
        self.randomized = temp