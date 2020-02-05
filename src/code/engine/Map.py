import pygame
import pytmx
from src.Settings import *


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * TILESIZE
        self.height = self.tmx.height * TILESIZE

    def render(self, surface):
        ti = self.tmx.get_tile_image_by_gid
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                        surface.blit(tile, (x * TILESIZE, y * TILESIZE))

    def create(self):
        surface = pygame.Surface((self.width, self.height))
        self.render(surface)
        return surface
