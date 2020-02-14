import math

import pytmx
import time
from src.Settings import *
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate
from src.code.pathfinding.Node import Node


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)

        mapWidth = self.tmx.width * self.tmx.tilewidth
        mapHeight = self.tmx.height * self.tmx.tileheight
        SETTINGS.configure(mapWidth, mapHeight)

        # This creates an 2D array, very quickly, through copying the same immutable object over and over again
        rows, cols = (mapWidth, mapHeight)
        SETTINGS.Graph = [x[:] for x in [[0] * rows] * cols]

        self.loadPath()
        self.start = vec2(0, 0)
        self.end = vec2(0, 0)

    def loadPath(self):
        startTime = time.time()

        pathLayer = self.tmx.get_layer_by_name("Path")
        backgroundLayer = self.tmx.get_layer_by_name("Background")
        ti = self.tmx.get_tile_image_by_gid

        SETTINGS.TilesAll = []
        SETTINGS.PathTiles = []
        SETTINGS.ObstacleTiles = []
        #SETTINGS.BuildingObjects = []
        SETTINGS.BackgroundTIles = []

        #if SETTINGS.CURRENT_LEVEL == 4:
        #    buildingLayer = self.tmx.get_object_by_name("BuildingObjects")
        #    for x, y, gid in buildingLayer:
        #        tile = ti(gid)
        #        if tile:
        #            tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
        #            tileObj.addImage(tile)
        #            SETTINGS.BuildingObjects.append(tileObj)
        #            SETTINGS.Graph[gid] = tileObj

        for x, y, gid in backgroundLayer:
            tile = ti(gid)
            if tile:
                tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
                tileObj.addImage(tile)
                SETTINGS.BackgroundTIles.append(tileObj)

        for x, y, gid in pathLayer:
            tile = ti(gid)
            if tile:
                position = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])

                tileObj = Tile(position, gid)
                tileObj.addImage(tile)
                SETTINGS.PathTiles.append(tileObj)

                nodeObj = Node(position)
                SETTINGS.Graph[y][x] = nodeObj

        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
                    tileObj.addImage(tile)
                    SETTINGS.TilesAll.append(tileObj)

        temp = []
        #print(str(type(SETTINGS.Graph)))
        for x in SETTINGS.Graph:
            row = []
            for y in x:
                if str(y) != "0":
                    row.append(y)
            if len(row) > 0:
                temp.append(row)

        SETTINGS.Graph = temp
        for col in range(len(SETTINGS.Graph)):
            for row in range(len(SETTINGS.Graph[col])):
                SETTINGS.Graph[col][row].addNeighbours()

        for col in temp:
            print(str(col))

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
