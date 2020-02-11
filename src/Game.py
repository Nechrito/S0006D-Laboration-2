from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.ai.behaviour.Global import Global
from src.code.ai.behaviour.states.CollectState import Collect
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.environment.Map import Map
from src.code.engine.Renderer import Renderer
from src.code.environment.Tile import Tile

from src.code.math.Vector import vec2
from src.code.pathfinding.PathManager import PathManager, getFullPath


class Game:

    def getRealFilePath(self, fileName):
        return path.join(self.directory, self.folder + fileName)

    def __init__(self, directory, folder):
        self.directory = directory
        self.folder = folder

        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

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

        self.mapLevel = 1
        self.agents = []
        self.agentGroup = pygame.sprite.Group()

        self.activePaths = []
        self.activeChildren = []
        self.updateSettings()

        self.font = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

    def loadMap(self, index):
        self.mapLevel = index

        if index == 1:
            self.updateSettings()
            self.map = Map(self.getRealFilePath(SETTINGS.MAP_1))
            self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF1))

        elif index == 2:
            self.updateSettings()
            self.map = Map(self.getRealFilePath(SETTINGS.MAP_2))
            self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF2))

        elif index == 3:
            self.updateSettings(26, 832, 832)
            self.map = Map(self.getRealFilePath(SETTINGS.MAP_3))
            self.map.loadReferenceMap(self.getRealFilePath(SETTINGS.MAP_REF3))

        elif index == 4:
            self.updateSettings(26, 880, 880)
            self.map = Map(self.getRealFilePath(SETTINGS.MAP_OLD))

        entityImg = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))
        entityImg = pygame.transform.scale(entityImg, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))

        self.agentGroup = pygame.sprite.Group()
        self.agents = [Entity("John", Collect(), Global(), self.agentGroup, entityImg, self.map.start)]
        self.agentGroup.add(self.agents)

        self.setEnd(self.map.end)
        self.setStart(self.map.start)

        self.obstacleImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_OBSTACLE))
        self.obstacleImg = pygame.transform.scale(self.obstacleImg, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))

        self.startImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))

        self.goalImg = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, (SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))

        CameraInstance.init(SETTINGS.SCREEN_WIDTH, SETTINGS.TILE_HEIGHT)
        self.renderer = Renderer(self.surface)

        self.updatePaths()

    def updateSettings(self, tileSize=16, width=768, height=768):

        SETTINGS.SCREEN_WIDTH = width
        SETTINGS.SCREEN_HEIGHT = height

        SETTINGS.TILE_WIDTH = width // tileSize
        SETTINGS.TILE_HEIGHT = height // tileSize
        SETTINGS.SCREEN_RESOLUTION = [SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT]

        SETTINGS.GRID_BOUNDS = (SETTINGS.TILE_WIDTH + SETTINGS.TILE_WIDTH // 2, SETTINGS.TILE_HEIGHT + SETTINGS.TILE_HEIGHT // 2)
        self.surface = pygame.display.set_mode(SETTINGS.SCREEN_RESOLUTION)

    def updatePaths(self):

        temp = PathManager()
        self.activePaths = temp.requestPath(self.startPos, self.endPos)
        if len(self.activePaths) <= 1:
            return

        self.activeChildren = temp.requestChildren()

        for i in range(0, len(self.activeChildren)):
            node = self.activeChildren[i]
            covered = getFullPath(self.activeChildren, i)
            total = getFullPath(self.activeChildren, 0)
            node.updateColors(covered, total)

        for tile in SETTINGS.Tiles:
            tile.isWalkable = tile.validate()

        for agent in self.agents:
            agent.setPath(self.activePaths)

    def setStart(self, pos: vec2):
        self.startPos = pos
        for agent in self.agents:
            agent.position = self.startPos

    def setEnd(self, pos: vec2):
        self.endPos = pos
        for agent in self.agents:
            agent.target = self.endPos

    def update(self):
        if not self.paused:
            pygame.display.set_caption(SETTINGS.TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(
                self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

        if not self.realCursorEnabled:
            self.cursor = pygame.mouse.get_pos()

        CameraInstance.followTarget(self.agents[0])
        for agent in self.agents:
            agent.moveTo(self.endPos)
            agent.update()
            if self.mapLevel >= 4:
                agent.updateState()

    def draw(self):

        self.renderer.clear()

        #  background
        for tile in self.map.tileSprites:
            self.renderer.renderTile(tile.image, vec2(tile.position.X * SETTINGS.TILE_WIDTH, tile.position.Y * SETTINGS.TILE_HEIGHT))
            #self.surface.blit(tile[1], (tile[0][0] * SETTINGS.TILE_WIDTH, tile[0][1] * SETTINGS.TILE_HEIGHT))

       # self.renderer.renderGrid()

        intersection = self.selectedTile()
        if intersection:
            self.renderer.renderRect((SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT), intersection.position.tuple)

        for obstacle in SETTINGS.ObstacleTiles:
            self.renderer.renderTile(self.obstacleImg, obstacle.position)

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.endPos)

        if self.mapLevel <= 4:

            # children
            for child in self.activeChildren:
                if child.position == self.endPos or child.position == self.startPos:
                    continue

                self.renderer.renderRect((SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT), child.position.tuple, child.color)

            # path tile
            for i in range(1, len(self.activePaths) - 1):
                node = self.activePaths[i]
                self.renderer.renderRect((SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT), node.position.tuple, node.color, 255)

            # path line
            for i in range(1, len(self.activePaths) - 1):
                waypoint1 = self.activePaths[i]
                waypoint2 = self.activePaths[i + 1]
                pygame.draw.line(self.surface, (255, 255, 255),
                                 (waypoint1.position + SETTINGS.TILE_WIDTH / 2).tuple,
                                 (waypoint2.position + SETTINGS.TILE_HEIGHT / 2).tuple)

            # agents path
            for agent in self.agents:
                waypoint1 = (agent.position.X + SETTINGS.TILE_WIDTH / 2, agent.position.Y + SETTINGS.TILE_HEIGHT / 2)
                waypoint2 = (agent.nextNode.X + SETTINGS.TILE_WIDTH / 2, agent.nextNode.Y + SETTINGS.TILE_HEIGHT / 2)
                pygame.draw.line(self.surface, (152, 52, 152), waypoint1, waypoint2, 5)

        if not self.realCursorEnabled:
            self.renderer.renderRect((self.cursorSize, self.cursorSize), (self.cursor[0] + self.cursorSize, self.cursor[1] + self.cursorSize), (37, 37, 38), 200)

        for agentSprite in self.agentGroup:
            self.surface.blit(agentSprite.image, agentSprite)

        self.clock.tick(SETTINGS.FPS)

    def selectedTile(self, position: vec2 = None) -> Tile:
        if not position:
            position = vec2(self.cursor[0] + self.cursorSize * 2, self.cursor[1] + self.cursorSize * 2)

        for tile in SETTINGS.Tiles:
            if tile.rect.collidepoint(position.tuple):
                return tile

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
