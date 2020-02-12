import pygame

from src.Settings import *
from src.code.math.cMath import lerp
from src.code.math.Vector import vec2


class Tile:

    def __init__(self, position: vec2, gid = -1):
        self.ID = gid

        self.position = position
        self.rect = pygame.Rect(position.X, position.Y, SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT)
        self.color = (58, 58, 57)
        self.isWalkable = self.validate()
        self.neighbours = []

    def __hash__(self):
        return hash(self.position) + hash(self.neighbours)

    def __cmp__(self, other):
        return self.ID != other.ID

    def __eq__(self, other):
        return self.position == other.position

    def addImage(self, img):
        self.image = img
        self.rect = self.image.get_rect()

    def addNeighbour(self):

        adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                    vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

        for direction in adjacent:
            neighbour = self.position + vec2(direction.X * SETTINGS.TILE_WIDTH, direction.Y * SETTINGS.TILE_HEIGHT)

            if neighbour not in self.neighbours:
                if 0 < neighbour.X < SETTINGS.SCREEN_WIDTH and 0 < neighbour.Y < SETTINGS.SCREEN_HEIGHT:
                    self.neighbours.append(neighbour)

    def validate(self):

        for obstacle in SETTINGS.ObstacleTiles:
            if self.rect.colliderect(obstacle.rect):
                return False

        if 0 < self.position.X < SETTINGS.SCREEN_WIDTH - SETTINGS.TILE_WIDTH and 0 < self.position.Y < SETTINGS.SCREEN_HEIGHT - SETTINGS.TILE_HEIGHT:
            return True

        return False

    def updateColors(self, distanceCovered, distanceTotal):
        delta = 1.0 / (distanceTotal / max(0.01, distanceCovered))
        colorMax = 240
        colorMin = 75
        colorByDist = ((lerp(colorMin, colorMax, delta)), (lerp(colorMax, colorMax / 4, delta)), (lerp(180, 255, delta)))
        self.color = colorByDist
        return self.color
