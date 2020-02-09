import pygame
import pytmx

from src.Settings import SETTINGS
from src.code.environment.Tile import Tile
from src.code.math.Iterator import fori
from src.code.math.Vector import vec2


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * SETTINGS.TILE_WIDTH
        self.height = self.tmx.height * SETTINGS.TILE_HEIGHT
        self.tileSprites = []

        ti = self.tmx.get_tile_image_by_gid
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))
                        self.tileSprites.append(((x, y), tile))

        self.start = vec2(0, 0)
        self.goal = vec2(0, 0)

        SETTINGS.MapTiles.clear()
        SETTINGS.ObstacleTiles.clear()

        tWidth = SETTINGS.TILE_WIDTH
        tHeight = SETTINGS.TILE_HEIGHT
        bounds = SETTINGS.GRID_BOUNDS

        # initialize grid
        i = 1
        for x in fori(tWidth, SETTINGS.SCREEN_WIDTH - bounds[0], tWidth):
            for y in fori(tHeight, SETTINGS.SCREEN_HEIGHT - bounds[1], tHeight):
                tile = Tile(vec2(x, y))
                tile.addNeighbour()
                SETTINGS.MapTiles.append(tile)
                i += 1

    def loadReferenceMap(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()[1:-1]
            y = 1
            for line in lines:
                x = 1
                line = line[1:-2]
                for char in line:
                    if char == 'X':
                        SETTINGS.ObstacleTiles.append(Tile(vec2(x * SETTINGS.TILE_WIDTH, y * SETTINGS.TILE_HEIGHT)))
                    if char == 'S':
                        self.start = vec2(x * SETTINGS.TILE_WIDTH, y * SETTINGS.TILE_HEIGHT)
                    if char == 'G':
                        self.goal = vec2(x * SETTINGS.TILE_WIDTH, y * SETTINGS.TILE_HEIGHT)

                    x += 1
                y += 1

    def render(self, surface):

        for tile in self.tileSprites:
            surface.blit(tile[1], (tile[0][0] * SETTINGS.TILE_WIDTH, tile[0][1] * SETTINGS.TILE_HEIGHT))
