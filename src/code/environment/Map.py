import pytmx
import time
from src.Settings import SETTINGS
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)

        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        SETTINGS.ObstacleTiles.clear()

        self.tileSprites = []
        self.bgSprites = []
        self.loadPath()
        self.start = vec2(0, 0)
        self.end = vec2(0, 0)

    def loadPath(self):
        startTime = time.time()

        pathLayer = self.tmx.get_layer_by_name("Path")
        backgroundLayer = self.tmx.get_layer_by_name("Background")
        ti = self.tmx.get_tile_image_by_gid

        cached = []
        SETTINGS.PathTiles = []

        for x, y, gid in pathLayer:
            tile = ti(gid)
            if tile:
                cached.append(gid)
                tileObj = Tile(vec2(x, y), gid)
                tileObj.addImage(tile)
                tileObj.addNeighbour()
                SETTINGS.PathTiles.append(tileObj)

        for x, y, gid in backgroundLayer:
            tile = ti(gid)
            if tile:
                cached.append(gid)
                tileObj = Tile(vec2(x, y), gid)
                tileObj.addImage(tile)
                self.bgSprites.append(tileObj)

        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:

                if cached and gid in cached:
                    continue

                tile = ti(gid)
                if tile:
                    tileObj = Tile(vec2(x, y), gid)
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
                        SETTINGS.ObstacleTiles.append(Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])))
                    if char == 'S':
                        self.start = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])
                    if char == 'G':
                        self.end = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])

                    x += 1
                y += 1
