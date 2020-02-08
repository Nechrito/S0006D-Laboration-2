import pygame

from src.Settings import TILE_SIZE, ObstacleTiles, SCREEN_WIDTH, OUTER_GRID, SCREEN_HEIGHT
from src.code.math.cMath import lerp
from src.code.math.vec2 import vec2


class Tile:
    def __init__(self, position: vec2):
        self.position = position
        self.rect = pygame.Rect(position.x, position.y, TILE_SIZE, TILE_SIZE)

        self.isWalkable = self.validate()
        self.weight = 1.0

        self.color = self.updateColors()

    def validate(self):

        for obstacle in ObstacleTiles:
            if self.rect.colliderect(obstacle.rect):
                self.isWalkable = False
                return self.isWalkable

        if self.position.x > SCREEN_WIDTH - OUTER_GRID or self.position.x < TILE_SIZE:
            self.isWalkable = False
            return self.isWalkable

        if self.position.y > SCREEN_HEIGHT - OUTER_GRID or self.position.y < TILE_SIZE:
            self.isWalkable = False
            return self.isWalkable

        return True

    def updateColors(self):
        end = vec2(SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE)

        dx = (abs(self.position.x - end.x) / end.x)
        dy = (abs(self.position.y - end.y) / end.y)

        colorByDist = ( (lerp(0, 176, dx)), (lerp(0, 255, dy)), 176 )

        self.color = colorByDist
        return self.color