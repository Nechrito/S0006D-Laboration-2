import pygame

from src.Settings import SETTINGS
from src.code.math.Vector import vec2
from src.code.math.cMath import lerp


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.color = (58, 58, 57)
        self.rect = pygame.Rect(position.X, position.Y, SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1])
        self.isWalkable = True
        self.neighbours = []

    def __repr__(self):
        return '(' + str(self.position.LocalX) + ", " + str(self.position.LocalY) + ')'

    def setParent(self, parent):
        self.parent = parent

    def addNeighbours(self):

        adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                    vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

        for direction in adjacent:
            neighbour = self.position + vec2(direction.X * SETTINGS.TILE_SCALE[0], direction.Y * SETTINGS.TILE_SCALE[1])

            node = SETTINGS.getNode(neighbour)
            if node:
                SETTINGS.Graph[neighbour.LocalX - 1][neighbour.LocalY - 1].setParent(self)
                self.neighbours.append(node)
            else:
                print("not valid neighbour at:")
                neighbour.log()



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

    def __lt__(self, other):
        return self.f < other.f

