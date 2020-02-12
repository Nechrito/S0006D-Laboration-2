import pygame
import pytmx
import time
from src.Settings import SETTINGS
from src.code.environment.Tile import Tile
from src.code.math.Iterator import fori
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * SETTINGS.TILE_WIDTH
        self.height = self.tmx.height * SETTINGS.TILE_HEIGHT
        self.tileSprites = []
        self.bgSprites = []
        self.tilePath = []
        self.loadPath()

        self.start = vec2(0, 0)
        self.end = vec2(0, 0)

        SETTINGS.Tiles.clear()
        SETTINGS.ObstacleTiles.clear()

        tWidth = SETTINGS.TILE_WIDTH
        tHeight = SETTINGS.TILE_HEIGHT
        bounds = SETTINGS.GRID_BOUNDS

        # initialize grid
        for x in fori(tWidth, SETTINGS.SCREEN_WIDTH - bounds[0], tWidth):
            for y in fori(tHeight, SETTINGS.SCREEN_HEIGHT - bounds[1], tHeight):
                tile = Tile(vec2(x, y))
                tile.addNeighbour()
                SETTINGS.Tiles.append(tile)

    def loadPath(self):
        startTime = time.time()

        pathLayer = self.tmx.get_layer_by_name("Path")
        backgroundLayer = self.tmx.get_layer_by_name("Background")
        ti = self.tmx.get_tile_image_by_gid

        for x, y, gid in pathLayer:
            tile = ti(gid)
            if tile:
                tile = pygame.transform.scale(tile, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))
                tileObj = Tile(vec2(x, y), gid)
                tileObj.addImage(tile)
                self.tilePath.append(tileObj)

        cached = []
        for x, y, gid in backgroundLayer:
            tile = ti(gid)
            if tile:
                cached.append(gid)
                tile = pygame.transform.scale(tile, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))
                tileObj = Tile(vec2(x, y), gid)
                tileObj.addImage(tile)
                self.bgSprites.append(tileObj)

        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:

                if cached and gid in cached:
                    continue

                isAlreadyCached = False
                for pathTile in self.tilePath:
                    if pathTile.ID == gid:
                        isAlreadyCached = True
                        break

                if isAlreadyCached:
                    continue

                tile = ti(gid)
                if tile:
                    tile = pygame.transform.scale(tile, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))
                    tileObj = Tile(vec2(x, y))
                    tileObj.addImage(tile)
                    self.tileSprites.append(tileObj)

        timeElapsed = time.time() - startTime
        print("Loaded map in: " + str(truncate(timeElapsed * 1000)) + "ms")

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
                        self.end = vec2(x * SETTINGS.TILE_WIDTH, y * SETTINGS.TILE_HEIGHT)

                    x += 1
                y += 1


