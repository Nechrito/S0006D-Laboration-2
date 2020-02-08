import pygame

from src.Settings import *
from src.code.math.cMath import lerp
from src.code.math.Vector import vec2


class Tile:
    def __init__(self, position: vec2):
        self.position = position
        self.rect = pygame.Rect(position.X, position.Y, SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT)
        self.color = self.updateColors()
        self.isWalkable = self.validate()
        self.weight = 1.0

    def validate(self):

        for obstacle in SETTINGS.ObstacleTiles:
            if self.rect.colliderect(obstacle.rect):
                self.isWalkable = False
                return self.isWalkable

        if self.position.X > SETTINGS.SCREEN_WIDTH - SETTINGS.GRID_BOUNDS[0] or self.position.X < SETTINGS.TILE_WIDTH:
            self.isWalkable = False
            return self.isWalkable

        if self.position.Y > SETTINGS.SCREEN_HEIGHT - SETTINGS.GRID_BOUNDS[1] or self.position.Y < SETTINGS.TILE_HEIGHT:
            self.isWalkable = False
            return self.isWalkable

        return True

    def updateColors(self):
        end = vec2(SETTINGS.SCREEN_WIDTH - SETTINGS.TILE_WIDTH, SETTINGS.SCREEN_HEIGHT - SETTINGS.TILE_HEIGHT)

        dx = (abs(self.position.X - end.X) / end.X)
        dy = (abs(self.position.Y - end.Y) / end.Y)
        colorByDist = ((lerp(0, 255, dx)), (lerp(0, 255, dy)), (lerp(100, 255, dx)))

        self.color = colorByDist
        return self.color
