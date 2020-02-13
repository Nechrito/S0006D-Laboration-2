from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.ai.behaviour.Global import Global
from src.code.ai.behaviour.states.CollectState import Collect
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Renderer import Renderer
from src.code.environment.AllBuildings import *
from src.code.environment.Map import Map
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2
from src.code.pathfinding.PathManager import getFullPath


class Game:

    def getRealFilePath(self, fileName):
        return path.join(self.directory, self.folder + fileName)

    def __init__(self, directory, folder):
        self.directory = directory
        self.folder = folder

        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        self.surface = pygame.display.set_mode((768, 768))
        self.renderer = Renderer(self.surface)

        logo = pygame.image.load(self.getRealFilePath(SETTINGS.ICON_PATH))
        pygame.display.set_icon(logo)

        pygame.display.set_caption(SETTINGS.TITLE)

        self.clock = pygame.time.Clock()
        self.paused = False

        self.cursor = pygame.mouse.get_pos()
        self.cursorSize = 9

        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        self.startPos = vec2()
        self.endPos = vec2()

        self.agents = []
        self.buildings = []

        self.activePaths = []
        self.activeChildren = []

        self.loadMap(1)

    def loadMap(self, index):
        SETTINGS.CURRENT_LEVEL = index

        self.agents = []
        self.buildings = []

        if index == 4:
           # SETTINGS.SCREEN_WIDTH = 1024
           # SETTINGS.SCREEN_HEIGHT = 768
            self.map = Map(self.getRealFilePath(SETTINGS.MAP_OLD))
            self.scaleAssets()

            self.buildings = (getClub(), getDrink(), getResturant(), getStore(),
                              getStackHQ(), getHotel(), getHangout(), getLTU())

            self.agents = [Entity("Alex", Collect(), Global(), self.entityImg, self.selectedTile(vec2(496, 404)).position)]
                           #Entity("Wendy", Collect(), Global(), self.entityImg, vec2(150, 610)),
                           #Entity("John", Collect(), Global(), self.entityImg, vec2(700, 380)),
                           #Entity("James", Collect(), Global(), self.entityImg, vec2(940, 400))]

        else:

            if index == 1:
                self.map = Map(self.getRealFilePath(SETTINGS.MAP_1))
                self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF1))
                self.scaleAssets()

            elif index == 2:
                self.map = Map(self.getRealFilePath(SETTINGS.MAP_2))
                self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF2))
                self.scaleAssets()

            elif index == 3:
                SETTINGS.SCREEN_WIDTH = SETTINGS.SCREEN_HEIGHT = 832
                self.map = Map(self.getRealFilePath(SETTINGS.MAP_3))
                self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF3))
                self.scaleAssets()

            self.agents = [Entity("John", Collect(), Global(), self.entityImg, self.map.start)]
            self.setEnd(self.map.end)
            self.setStart(self.map.start)

        CameraInstance.init()
        self.surface = pygame.display.set_mode((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT))
        self.renderer = Renderer(self.surface)

        self.updatePaths()

    def scaleAssets(self):

        self.font = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        scale = SETTINGS.TILE_SCALE
        self.entityImg = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))
        self.entityImg = pygame.transform.scale(self.entityImg, scale)

        self.obstacleImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_OBSTACLE))
        self.obstacleImg = pygame.transform.scale(self.obstacleImg, scale)

        self.startImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, scale)

        self.goalImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, scale)

    def updatePaths(self):
        if SETTINGS.CURRENT_LEVEL == 4:
            return

        for col in range(len(SETTINGS.Graph)):
            for row in range(len(SETTINGS.Graph[col])):
                SETTINGS.Graph[col][row].isWalkable = SETTINGS.Graph[col][row].validate()
                SETTINGS.Graph[col][row].addNeighbours()

        self.agents[0].moveTo(self.endPos)
        self.activePaths = self.agents[0].waypoints
        if not self.activePaths or len(self.activePaths) <= 2:
            return

        self.activeChildren = self.agents[0].pathfinder.requestChildren()

        total = getFullPath(self.activeChildren, 0)
        for i in range(0, len(self.activeChildren)):
            covered = getFullPath(self.activeChildren, i)
            self.activeChildren[i].updateColors(covered, total)

    def setStart(self, pos: vec2):
        self.startPos = self.selectedTile(pos).position
        if self.endPos:
            self.agents[0].setStart(self.startPos, self.endPos)

    def setEnd(self, pos: vec2):
        self.endPos =pos #self.selectedTile().position

    def update(self):

        vec2(self.cursor).log()

        if not self.paused:
            pygame.display.set_caption(SETTINGS.TITLE +
                                       " | Speed: " +
                                       str(GameTime.timeScale) +
                                       " | FPS " +
                                       "{:.0f}".format(self.clock.get_fps()) +
                                       " | Date: " + GameTime.timeElapsed())

        if not self.realCursorEnabled:
            self.cursor = pygame.mouse.get_pos()

        for agent in self.agents:
            agent.moveTo(self.endPos)
            agent.update()

            if SETTINGS.CURRENT_LEVEL >= 4:
                agent.updateState()

        CameraInstance.followTarget(self.agents[0])

    def draw(self):

        self.renderer.clear()

        for tile in SETTINGS.BackgroundTIles:
            self.renderer.renderTileImg(tile.image, tile.position)

        for tile in SETTINGS.PathTiles:
            self.renderer.renderTileImg(tile.image, tile.position)

        for tile in SETTINGS.TilesAll:
            self.renderer.renderTileImg(tile.image, tile.position)

        self.renderer.renderGrid()

        if SETTINGS.CURRENT_LEVEL <= 3:

            for obstacle in SETTINGS.ObstacleTiles:
                self.renderer.renderTileImg(self.obstacleImg, obstacle.position)

            self.renderer.renderTileImg(self.startImg, self.startPos)
            self.renderer.renderTileImg(self.goalImg, self.endPos)

            if self.activePaths:
                # children
                for child in self.activeChildren:
                    if child.position == self.endPos or child.position == self.startPos:
                        continue

                    self.renderer.renderRect((SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1]), child.position.tuple, child.color)

                # path line
                for i in range(1, len(self.activePaths) - 1):
                    waypoint1 = self.activePaths[i]
                    waypoint2 = self.activePaths[i + 1]
                    self.renderer.renderLine((waypoint1.position + SETTINGS.TILE_SCALE[0] / 2).tuple,
                                             (waypoint2.position + SETTINGS.TILE_SCALE[1] / 2).tuple)

                # agents path
                for agent in self.agents:
                    waypoint1 = vec2(agent.position.X + SETTINGS.TILE_SCALE[0] / 2, agent.position.Y + SETTINGS.TILE_SCALE[1] / 2)
                    waypoint2 = vec2(agent.nextNode.X + SETTINGS.TILE_SCALE[0] / 2, agent.nextNode.Y + SETTINGS.TILE_SCALE[1] / 2)
                    self.renderer.renderLine(waypoint1, waypoint2, (152, 52, 152), 5)

        intersection = self.selectedTile()

        if intersection:
            self.renderer.renderRect(SETTINGS.TILE_SCALE, intersection.position.tuple)

        if not self.realCursorEnabled:
            self.renderer.renderRect((self.cursorSize, self.cursorSize), (self.cursor[0] + self.cursorSize, self.cursor[1] + self.cursorSize), (37, 37, 38), 200)

        for agent in self.agents:
            self.renderer.renderTileImg(agent.image, agent.position)

        self.clock.tick(SETTINGS.MAX_FPS)

    def selectedTile(self, location: vec2 = None):
        if not location:
            location = vec2(self.cursor[0] + self.cursorSize * 2, self.cursor[1] + self.cursorSize * 2)

        for tile in SETTINGS.PathTiles:
            if tile.rect.collidepoint(location.tuple):
                return tile

        closest = None
        distance = 0
        for tile in SETTINGS.PathTiles:
            currentDist = tile.position.distance(location)
            if currentDist < distance or distance == 0:
                distance = currentDist
                closest = tile

        return closest

    def isObstacle(self, tile: Tile):
        for obstacle in SETTINGS.ObstacleTiles:
            if tile.rect.colliderect(obstacle.rect):
                return obstacle
        return None

    def setObstacle(self):
        tile = self.selectedTile()

        if not tile:
            return None

        obstacle = self.isObstacle(tile)

        if obstacle:
            SETTINGS.ObstacleTiles.remove(obstacle)
        else:
            SETTINGS.ObstacleTiles.append(tile)
