import pygame
import pytmx

from src.Settings import *
from src.code.environment.Tile import Tile
from src.code.math.iterator import fori
from src.code.math.vec2 import vec2


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * TILE_SIZE
        self.height = self.tmx.height * TILE_SIZE
        MapTiles.clear()
        ObstacleTiles.clear()

        i = 1
        for x in fori(TILE_SIZE, SCREEN_WIDTH - TILE_SIZE - TILE_SIZE / 2, TILE_SIZE):
            for y in fori(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE - TILE_SIZE / 2, TILE_SIZE):
                MapTiles.append(Tile(vec2(x, y)))
                i += 1

    def addObstaclesFromFile(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()[1:-1]
            y = 1
            for line in lines:
                x = 1
                line = line[1:-2]
                for char in line:
                    if char == 'X':
                        ObstacleTiles.append(Tile(vec2(x, y) * TILE_SIZE))
                    x += 1
                y += 1

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
