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

        self.wallImg = pygame.image.load(getRealFilePath(TILE_WALL))
        self.wallImg = pygame.transform.scale(self.wallImg, (TILESIZE, TILESIZE))

        self.startImg = pygame.image.load(getRealFilePath(TILE_START))
        self.startImg = pygame.transform.scale(self.startImg, (TILESIZE, TILESIZE))

        self.goalImg = pygame.image.load(getRealFilePath(TILE_GOAL))
        self.goalImg = pygame.transform.scale(self.goalImg, (TILESIZE, TILESIZE))

    def load(self):

        self.renderer = Renderer(self.surface)

        self.map = Map(getRealFilePath(MAP_1))
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
            pygame.display.set_caption(TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

        GameTime.updateTicks()

        if not self.realCursorEnabled:
            self.cursor = pygame.mouse.get_pos()

    def draw(self):

        self.renderer.clear()

        self.map.render(self.surface)
        self.renderer.renderGrid()

        self.renderer.renderTile(self.startImg, self.startPos)
        self.renderer.renderTile(self.goalImg, self.goalPos)

        self.renderer.renderText("START", (self.startPos[0] + 24, self.startPos[1]), self.fontBold)
        self.renderer.renderText("GOAL", (self.goalPos[0] + 24, self.goalPos[1]), self.fontBold)

        if not self.realCursorEnabled:
            self.renderer.renderRect((16, 16), self.cursor, (37, 37, 38), 200)

        self.clock.tick(FPS)
