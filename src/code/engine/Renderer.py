import pygame
import pygame.freetype
from src.Settings import *
from src.code.engine.Camera import CameraInstance
from src.code.environment.Tile import Tile
from src.code.math.Iterator import fori


class Renderer:

    def __init__(self, surface):
        self.surface = surface
        self.texts = []

    def clear(self):
        pygame.display.update()
        self.surface.fill((200, 200, 200))

    def renderTileImg(self, img, pos):
        self.surface.blit(img, CameraInstance.centeredVec(pos))

    def renderTile(self, tile: Tile):
        pos = vec2(tile.position.X * SETTINGS.TILE_SCALE[0], tile.position.Y * SETTINGS.TILE_SCALE[1])
        self.surface.blit(tile.image, CameraInstance.centeredVec(pos))

    def renderRect(self, size, pos, color=(255, 255, 255), alpha=128):
        surface = pygame.Surface(size)
        surface.set_alpha(alpha)
        surface.fill(color)

        if SETTINGS.MAP_LEVEL >= 4:
            self.surface.blit(surface, CameraInstance.centeredVec(pos))
        else:
            self.surface.blit(surface, pos)

    def renderGrid(self):
        tWidth = SETTINGS.TILE_SCALE[0]
        tHeight = SETTINGS.TILE_SCALE[1]
        sWidth = (SETTINGS.SCREEN_WIDTH - tWidth)
        sHeight = (SETTINGS.SCREEN_HEIGHT - tHeight)

        for x in fori(tWidth, sWidth, tWidth):
            self.renderLine((x, tHeight), (x, sHeight))
        for y in fori(tHeight, sHeight, tHeight):
            self.renderLine((tWidth, y), (sWidth, y))

    def renderLine(self, start, end, color=(255, 255, 255), width=1):
        pygame.draw.line(self.surface, color, CameraInstance.centeredVec(start), CameraInstance.centeredVec(end), width)

    def renderText(self, text: str, position, font, color=(255, 255, 255)):
        fontRendered, fontRect = font.render(text, color)
        self.surface.blit(fontRendered, (position[0] - fontRect[2] / 2, position[1] - fontRect[3] / 2))

    def renderTexts(self, position, font, color=(0, 0, 0)):
        if len(self.texts) <= 0:
            raise Exception("Use method .append(...) first to render multiple lines of text!")

        pos = (position[0], position[1])
        for line in range(len(self.texts)):
            msg = self.texts[line]
            self.renderText(msg, pos, font, color)
            pos = (pos[0], pos[1] + font.size + 2)

        self.texts.clear()

    def append(self, msg):
        self.texts.append(msg)
