import sys
from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Map import Map
from src.code.engine.Renderer import Renderer
from src.code.pathfinding.Algorithm import AStar

from src.code.math.vec2 import vec2


def getRealFilePath(fileName):
    if getattr(sys, 'frozen', False):
        directory = path.dirname(sys.executable)
        folder = "src/resources/"
    else:
        directory = path.dirname(__file__)
        folder = "resources/"

    return path.join(directory, folder + fileName)


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        logo = pygame.image.load(getRealFilePath(ICON_PATH))
        pygame.display.set_icon(logo)

        pygame.display.set_caption(TITLE)

        self.surface = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.font = pygame.freetype.Font(getRealFilePath(FONT_REGULAR), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))
        self.fontBold = pygame.freetype.Font(getRealFilePath(FONT_BOLD), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))

        self.grid = []
        self.obstacles = [vec2(3, 3), vec2(4, 3), vec2(5, 3), vec2(12, 2),
                          vec2(3, 4), vec2(4, 4), vec2(5, 4), vec2(12, 3),
                          vec2(3, 5), vec2(4, 5), vec2(5, 5), vec2(13, 2),
                          vec2(3, 6), vec2(4, 6), vec2(5, 6), vec2(13, 3),
                          vec2(3, 7), vec2(4, 7), vec2(5, 7),
                          vec2(12, 7), vec2(12, 8), vec2(12, 9),
                          vec2(11, 7), vec2(11, 8), vec2(11, 9),
                          vec2(10, 7), vec2(10, 8), vec2(10, 9),
                          vec2(11, 10), vec2(12, 10),
                          vec2(4, 13), vec2(5, 13), vec2(6, 13),
                          vec2(3, 14), vec2(4, 14), vec2(5, 14), vec2(6, 14), vec2(7, 14)]

        for i in range(len(self.obstacles)):
            self.obstacles[i] *= TILE_SIZE

        self.obstacleImg = pygame.image.load(getRealFilePath(TILE_OBSTACLE))
        self.obstacleImg = pygame.transform.scale(self.obstacleImg, (TILE_SIZE, TILE_SIZE))

        self.startImg = pygame.image.load(getRealFilePath(TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, (TILE_SIZE, TILE_SIZE))

        self.goalImg = pygame.image.load(getRealFilePath(TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, (TILE_SIZE, TILE_SIZE))

    def load(self):

        self.renderer = Renderer(self.surface)

        self.map = Map(getRealFilePath(MAP_1))
        self.map.addGrid(self.grid)

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

        self.pathfinder = AStar(self.grid, self.obstacles)
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
            self.renderer.renderRect2(intersection)

        for obstacle in self.obstacles:
            self.renderer.renderTile(self.obstacleImg, obstacle)

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.goalPos)

        if self.activePath and len(self.activePath) >= 1:
            for node in self.pathfinder.neighbours:
                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), (node.position.x, node.position.y), (37, 37, 38), 128)

            for i in range(1, len(self.activePath) - 1):
                node1 = self.activePath[i]
                node2 = self.activePath[i + 1]
                self.renderer.renderRect((TILE_SIZE, TILE_SIZE), (node1.x, node1.y), (37, 37, 38), 255)
                pygame.draw.line(self.surface, (237, 237, 238), (node1.x, node1.y), (node2.x, node2.y), 5)

        self.renderer.renderText("Start", (self.startPos.x + 24, self.startPos.y), self.fontBold)
        self.renderer.renderText("End", (self.goalPos.x + 24, self.goalPos.y), self.fontBold)

        if not self.realCursorEnabled:
            size = 16
            self.renderer.renderRect((size, size), (self.cursor[0] + size, self.cursor[1] + size), (37, 37, 38), 240)

        self.clock.tick(FPS)

    def updatePath(self):
        self.pathfinder = AStar(self.grid, self.obstacles)
        self.activePath = self.pathfinder.getPath(self.startPos, self.goalPos)

    def getSelectedSquare(self, pos=None):
        if not pos:
            pos = vec2(self.cursor[0] + TILE_SIZE / 2, self.cursor[1] + TILE_SIZE / 2)

        for rect in self.grid:
            if rect.collidepoint((pos.x, pos.y)):
                return rect
        return None

    def getSelectedObject(self, rect):
        for obstacle in self.obstacles:
            if rect[0] == obstacle[0] and rect[1] == obstacle[1]:
                return obstacle

        return None

    def setObstacle(self):
        rect = self.getSelectedSquare()

        if not rect:
            return None

        target = self.getSelectedObject(rect)

        if target:
            self.obstacles.remove(target)
        else:
            self.obstacles.append((rect[0], rect[1]))
