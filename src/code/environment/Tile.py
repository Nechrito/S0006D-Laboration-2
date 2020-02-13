import math

import pygame

from src.Settings import *
from src.code.math.cMath import lerp
from src.code.math.Vector import vec2


class Tile:

    def __init__(self, position: vec2, gid = -1):
        self.ID = gid
        self.position = position
        self.rect = pygame.Rect(position.X, position.Y, SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1])
        self.color = (58, 58, 57)
        self.isWalkable = self.validate()
        self.neighbours = []

    def __dir__(self):
        return ['ID', 'position']

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return (self.ID != -1 and self.ID == other.ID) or self.position == other.position

    def addImage(self, img):
        self.image = pygame.transform.scale(img, (SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1]))
        #self.rect = self.image.get_rect()

    def addNeighbour(self):

        adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                    vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

        for direction in adjacent:
            neighbour = self.position + vec2(direction.X * SETTINGS.TILE_SCALE[0], direction.Y * SETTINGS.TILE_SCALE[1])

            if neighbour not in self.neighbours:
                if 0 < neighbour.X < SETTINGS.SCREEN_WIDTH and 0 < neighbour.Y < SETTINGS.SCREEN_HEIGHT:
                    self.neighbours.append(neighbour)

    def validate(self):

        for obstacle in SETTINGS.ObstacleTiles:
            if self.rect.colliderect(obstacle.rect):
                return False

        if 0 < self.position.X < SETTINGS.SCREEN_WIDTH - SETTINGS.TILE_SCALE[0] and 0 < self.position.Y < SETTINGS.SCREEN_HEIGHT - SETTINGS.TILE_SCALE[1]:
            return True

        return False

    def updateColors(self, distanceCovered, distanceTotal):
        if distanceCovered == 0:
            distanceCovered = 0.1

        delta = min(1.0, max(0.001, distanceCovered / distanceTotal))
        colorMax = 255.0
        colorMin = 0.0
        colorByDist = ((lerp(colorMax, colorMax * 0.60, delta)), (lerp(colorMax * 0.05, colorMax * 0.70, delta)), (lerp(colorMax * 0.60, colorMax, delta)))
        self.color = colorByDist
        return self.color
