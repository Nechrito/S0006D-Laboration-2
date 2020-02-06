from math import sqrt

from src.code.engine.GameTime import GameTime
from src.code.math.cMath import cMath

import pygame
import pytmx
from src.Settings import *
from src.code.math.iterator import fori
from src.code.math.vec2 import vec2


class Square:
    def __init__(self, position: vec2, obstacles=None):
        self.walkable = True
        self.isObstacle = False
        self.position = position
        self.rect = pygame.Rect(position.x, position.y, TILE_SIZE, TILE_SIZE)
        self.weight = int(position.x + position.y)

        # todo
        self.alpha = cMath.lerp(0, 255 / sqrt(SCREEN_WIDTH * SCREEN_HEIGHT), position.length)

        self.color = (cMath.lerp(0, 255 / SCREEN_WIDTH, position.x),
                      cMath.lerp(0, 255 / SCREEN_HEIGHT, position.y),
                      cMath.lerp(0, 255 / (SCREEN_WIDTH + SCREEN_HEIGHT), position.x + position.y))

        self.update(obstacles)

    def __hash__(self):
        return hash(self.walkable) + hash(self.position) + hash(self.weight)

    def update(self, obstacles):

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.walkable = False
                self.isObstacle = True
                return

        if self.position.x < TILE_SIZE or self.position.x > SCREEN_WIDTH - (TILE_SIZE + int(TILE_SIZE / 2)):
            self.walkable = False
            return

        if self.position.y < TILE_SIZE or self.position.y > SCREEN_HEIGHT - (TILE_SIZE + int(TILE_SIZE / 2)):
            self.walkable = False
            return

        self.walkable = True


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * TILE_SIZE
        self.height = self.tmx.height * TILE_SIZE

    def addGrid(self, obstacles):
        index = 0
        temp = []
        for x in fori(TILE_SIZE, SCREEN_WIDTH - TILE_SIZE - TILE_SIZE / 2, TILE_SIZE):
            for y in fori(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE / 2, TILE_SIZE):
                index += 1
                temp.append(Square(vec2(x, y), obstacles))
        return temp

    def addObstacles(self):

        obstacles = [vec2(3, 3), vec2(4, 3), vec2(5, 3), vec2(12, 2),
                     vec2(3, 4), vec2(4, 4), vec2(5, 4), vec2(12, 3),
                     vec2(3, 5), vec2(4, 5), vec2(5, 5), vec2(13, 2),
                     vec2(3, 6), vec2(4, 6), vec2(5, 6), vec2(13, 3),
                     vec2(3, 7), vec2(4, 7), vec2(5, 7),
                     vec2(12, 7), vec2(12, 8), vec2(12, 9),
                     vec2(11, 7), vec2(11, 8), vec2(11, 9),
                     vec2(10, 7), vec2(10, 8), vec2(10, 9),
                     vec2(11, 10), vec2(12, 10),
                     vec2(4, 13), vec2(5, 13), vec2(6, 13),
                     vec2(3, 14), vec2(4, 14), vec2(5, 14), vec2(6, 14), vec2(7, 14)]

        temp = []
        for obstacle in obstacles:
            obstacle *= TILE_SIZE
            temp.append(Square(obstacle, temp))
        return temp

    def render(self, surface):
        ti = self.tmx.get_tile_image_by_gid
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                        surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

    def create(self):
        surface = pygame.Surface((self.width, self.height))
        self.render(surface)
        return surface
