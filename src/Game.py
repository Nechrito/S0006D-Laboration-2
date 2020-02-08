import sys
from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.environment.Map import Map
from src.code.engine.Renderer import Renderer
from src.code.pathfinding.PathManager import AStar

from src.code.math.vec2 import vec2


class Game:

    def getRealFilePath(self, fileName):
        return path.join(self.directory, self.folder + fileName)

    def __init__(self, directory, folder):
        self.directory = directory
        self.folder = folder

        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        logo = pygame.image.load(self.getRealFilePath(ICON_PATH))
        pygame.display.set_icon(logo)

        pygame.display.set_caption(TITLE)

        self.surface = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.font = pygame.freetype.Font(self.getRealFilePath(FONT_REGULAR), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(FONT_BOLD), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))

        self.obstacleImg = pygame.image.load(self.getRealFilePath(TILE_OBSTACLE))
        self.obstacleImg = pygame.transform.scale(self.obstacleImg, (TILE_SIZE, TILE_SIZE))

        self.startImg = pygame.image.load(self.getRealFilePath(TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, (TILE_SIZE, TILE_SIZE))

        self.goalImg = pygame.image.load(self.getRealFilePath(TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, (TILE_SIZE, TILE_SIZE))

    def load(self):

        self.renderer = Renderer(self.surface)

        self.clock = pygame.time.Clock()
        self.paused = False

        self.cursor = pygame.mouse.get_pos()
        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        self.loadMap(1)

    def loadMap(self, index):

        if index == 1:
            self.startPos = vec2(TILE_SIZE, TILE_SIZE)
            self.goalPos = vec2(TILE_SIZE * 14, TILE_SIZE * 14)
            self.map = Map(self.getRealFilePath(MAP_1))
            self.map.addObstaclesFromFile(self.getRealFilePath(MAP_REF1))
        elif index == 2:
            self.startPos = vec2(TILE_SIZE, TILE_SIZE)
            self.goalPos = vec2(TILE_SIZE * 14, TILE_SIZE * 14)
            self.map = Map(self.getRealFilePath(MAP_2))
            self.map.addObstaclesFromFile(self.getRealFilePath(MAP_REF2))

        elif index == 3:
            self.map = Map(self.getRealFilePath(MAP_3))

        self.mapImg = self.map.create()
        self.mapRect = self.mapImg.get_rect()

        self.camera = CameraInstance(self.map.width, self.map.height)

        self.pathfinder = AStar()
        self.updateMap()

    def update(self):

        if not self.paused:
            pygame.display.set_caption(TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(
                self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

        if not self.realCursorEnabled:
            self.cursor = pygame.mouse.get_pos()

    def draw(self):

        self.renderer.clear()
        self.map.render(self.surface)

        #self.renderer.renderGrid()

        intersection = self.selectedTile()
        if intersection:
            self.renderer.renderRect2(intersection.rect)

        for obstacle in ObstacleTiles:
            self.renderer.renderTile(self.obstacleImg, obstacle.position)

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.goalPos)

        if self.activePath:

            # path neighbours
            for node in self.pathfinder.children:
                if node.position == self.goalPos or node.position == self.startPos:
                    continue

                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), node.position.tuple, node.color)

            # path tile
            for i in range(1, len(self.activePath) - 1):
                node = self.activePath[i]
                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), node.position.tuple, node.color, 255)

            # path line
            for i in range(0, len(self.activePath) - 1):
                waypoint1 = self.activePath[i]
                waypoint2 = self.activePath[i + 1]
                pygame.draw.line(self.surface, (255, 255, 255), (waypoint1.position + TILE_SIZE / 2).tuple, (waypoint2.position + TILE_SIZE / 2).tuple, 2)

        if not self.realCursorEnabled:
            size = 18
            self.renderer.renderRect((size, size), (self.cursor[0] + size, self.cursor[1] + size), (37, 37, 38), 200)

        self.clock.tick(FPS)

    def updateMap(self):
        for i in range(0, len(MapTiles)):
            MapTiles[i].updateColors()
            MapTiles[i].validate()

        for i in range(0, len(ObstacleTiles)):
            ObstacleTiles[i].updateColors()
            ObstacleTiles[i].validate()

        self.activePath = self.pathfinder.getPath(self.startPos, self.goalPos)

    def selectedTile(self, pos=None):
        if not pos:
            pos = vec2(self.cursor[0] + TILE_SIZE / 2, self.cursor[1] + TILE_SIZE / 2)

        for tile in MapTiles:
            if tile.rect.collidepoint((pos.x, pos.y)):
                return tile
        return None

    def isObstacle(self, tile):
        for obstacle in ObstacleTiles:
            if tile.rect.colliderect(obstacle.rect):
                return obstacle

        return None

    def setObstacle(self):
        tile = self.selectedTile()

        if not tile:
            return None

        obstacle = self.isObstacle(tile)

        if obstacle:
            ObstacleTiles.remove(obstacle)
        else:
            ObstacleTiles.append(tile)
