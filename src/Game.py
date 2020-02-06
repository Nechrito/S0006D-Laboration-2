import sys
from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.environment.Map import Map
from src.code.engine.Renderer import Renderer
from src.code.pathfinding.Algorithm import AStar

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

        self.map = Map(self.getRealFilePath(MAP_1))

        self.obstacles = self.map.addObstacles()
        self.grid = self.map.addGrid(self.obstacles)

        self.mapImg = self.map.create()
        self.mapRect = self.mapImg.get_rect()

        GameTime.init()

        self.camera = CameraInstance(self.map.width, self.map.height)

        self.clock = pygame.time.Clock()
        self.paused = False

        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        self.cursor = pygame.mouse.get_pos()

        self.startPos = vec2(TILE_SIZE, TILE_SIZE)
        self.goalPos = vec2(TILE_SIZE * 14, TILE_SIZE * 14)

        self.pathfinder = AStar(self.obstacles)
        self.activePath = self.pathfinder.getPath(self.startPos, self.goalPos)

    def update(self):

        if not self.paused:
            pygame.display.set_caption(TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(
                self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

        GameTime.updateTicks()

        if not self.realCursorEnabled:
            self.cursor = pygame.mouse.get_pos()

    def draw(self):

        self.renderer.clear()

        self.map.render(self.surface)
        self.renderer.renderGrid()

        intersection = self.getSelectedSquare()
        if intersection:
            self.renderer.renderRect2(intersection.rect)

        for obstacle in self.obstacles:
            self.renderer.renderTile(self.obstacleImg, obstacle.position)

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.goalPos)

        self.renderer.renderText("Start", (self.startPos.x + 24, self.startPos.y), self.fontBold)
        self.renderer.renderText("End", (self.goalPos.x + 24, self.goalPos.y), self.fontBold)

        if self.activePath and len(self.activePath) >= 1:
            for node in self.pathfinder.children:
                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), (node.position.x, node.position.y), node.color, 128)

            for i in range(1, len(self.activePath) - 1):
                node1 = self.activePath[i]
                node2 = self.activePath[i + 1]
                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), (node1.x, node1.y), (37, 37, 38), 255)
                pygame.draw.line(self.surface, (237, 237, 238), (node1.x, node1.y), (node2.x, node2.y), 5)

        if not self.realCursorEnabled:
            size = 16
            self.renderer.renderRect((size, size), (self.cursor[0] + size, self.cursor[1] + size), (37, 37, 38), 240)

        self.clock.tick(FPS)

    def updateGrid(self):
        for i in range(0, len(self.obstacles)):
            self.obstacles[i].update(self.obstacles)

        for i in range(0, len(self.grid)):
            self.grid[i].update(self.obstacles)

        self.pathfinder.update(self.obstacles)
        self.activePath = self.pathfinder.getPath(self.startPos, self.goalPos)

    def getSelectedSquare(self, pos=None):
        if not pos:
            pos = vec2(self.cursor[0] + TILE_SIZE / 2, self.cursor[1] + TILE_SIZE / 2)

        for square in self.grid:
            if square.rect.collidepoint((pos.x, pos.y)):
                return square
        return None

    def getSelectedObject(self, square):
        for obstacle in self.obstacles:
            if square.rect.colliderect(obstacle.rect):
                return obstacle

        return None

    def setObstacle(self):
        square = self.getSelectedSquare()

        if not square:
            return None

        obstacle = self.getSelectedObject(square)

        if obstacle:
            self.obstacles.remove(obstacle)
        else:
            self.obstacles.append(square)
