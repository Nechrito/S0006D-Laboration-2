import sys
from os import path

import pygame
import pygame.freetype
from src.Settings import *
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Map import Map
from src.code.engine.Renderer import Renderer


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

        self.surface = pygame.display.set_mode(RESOLUTION)
        self.font = pygame.freetype.Font(getRealFilePath(FONT_REGULAR), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))
        self.fontBold = pygame.freetype.Font(getRealFilePath(FONT_BOLD), int(SCREEN_HEIGHT * 22 / SCREEN_WIDTH))

        self.grid = []
        self.obstacles = [(3, 3), (4, 3), (5, 3), (12, 2),
                          (3, 4), (4, 4), (5, 4), (12, 3),
                          (3, 5), (4, 5), (5, 5), (13, 2),
                          (3, 6), (4, 6), (5, 6), (13, 3),
                          (3, 7), (4, 7), (5, 7),
                          (12, 7), (12, 8), (12, 9),
                          (11, 7), (11, 8), (11, 9),
                          (10, 7), (10, 8), (10, 9),
                          (11, 10), (12, 10),
                          (4, 13), (5, 13), (6, 13),
                          (3, 14), (4, 14), (5, 14), (6, 14), (7, 14)]

        for i in range(len(self.obstacles)):
            self.obstacles[i] = (self.obstacles[i][0] * TILESIZE, self.obstacles[i][1] * TILESIZE)

        self.obstacleImg = pygame.image.load(getRealFilePath(TILE_OBSTACLE))
        self.obstacleImg = pygame.transform.scale(self.obstacleImg, (TILESIZE, TILESIZE))

        self.startImg = pygame.image.load(getRealFilePath(TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, (TILESIZE, TILESIZE))

        self.goalImg = pygame.image.load(getRealFilePath(TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, (TILESIZE, TILESIZE))

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

        self.startPos = (TILESIZE, TILESIZE)
        self.goalPos = (TILESIZE * 14, TILESIZE * 14)

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

        intersection = self.getIntersectedRect()
        if intersection:
            self.renderer.renderRect2(intersection)

        for i in range(0, len(self.obstacles)):
            self.renderer.renderTile(self.obstacleImg, self.obstacles[i])

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.goalPos)

        self.renderer.renderText("Start", (self.startPos[0] + 24, self.startPos[1]), self.fontBold)
        self.renderer.renderText("End", (self.goalPos[0] + 24, self.goalPos[1]), self.fontBold)

        if not self.realCursorEnabled:
            self.renderer.renderRect((TILESIZE / 2, TILESIZE / 2), self.cursor, (37, 37, 38), 128)

        self.clock.tick(FPS)

    def getIntersectedRect(self):
        for i in range(len(self.grid)):
            rect = self.grid[i]
            if rect.collidepoint((self.cursor[0] + TILESIZE / 2, self.cursor[1] + TILESIZE / 2)):
                return rect
        return None

    def getRectFrom(self, pos):
        for i in range(len(self.grid)):
            rect = self.grid[i]
            if rect.collidepoint(pos):
                return rect
        return None

    def getSelectedObject(self, rect):
        for i in range(len(self.obstacles)):
            obstacle = self.obstacles[i]
            x = obstacle[0]
            y = obstacle[1]

            if rect[0] == x and rect[1] == y:
                return obstacle

        return None

    def setObstacle(self):
        rect = self.getIntersectedRect()

        if not rect:
            return None

        target = self.getSelectedObject(rect)

        if target:
            self.obstacles.remove(target)
        else:
            self.obstacles.append((rect[0], rect[1]))
