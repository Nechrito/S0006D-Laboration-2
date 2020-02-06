import random


class Building:
    def __init__(self, position, name: str, description: str = None):
        self.position = position
        self.name = name
        self.description = description

        threshold = 30
        self.randomized = self.position[0] + random.randrange(-threshold, threshold), self.position[1] + random.randrange(-threshold, threshold / 2)