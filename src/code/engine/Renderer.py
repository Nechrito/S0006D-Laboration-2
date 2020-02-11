import pygame
import pygame.freetype
from src.Settings import *
from src.code.math.Iterator import fori


class Renderer:

    def __init__(self, surface):
        self.surface = surface
        self.texts = []

    def clear(self):
        pygame.display.update()
        self.surface.fill((52, 52, 52))

    def renderTile(self, image, position):
        self.surface.blit(image, position.tuple)

    def renderRect(self, size, pos, color=(255, 255, 255), alpha=128):
        surface = pygame.Surface(size)
        surface.set_alpha(alpha)
        surface.fill(color)
        self.surface.blit(surface, pos)

    def renderGrid(self):
        color = (222, 80, 146)
        tWidth = SETTINGS.TILE_WIDTH
        tHeight = SETTINGS.TILE_HEIGHT
        sWidth = SETTINGS.SCREEN_WIDTH - tWidth
        sHeight = SETTINGS.SCREEN_HEIGHT - tHeight

        for x in fori(tWidth, sWidth, tWidth):
            pygame.draw.line(self.surface, color, (x, tHeight), (x, sHeight))
        for y in fori(tHeight, sHeight, tHeight):
            pygame.draw.line(self.surface, color, (tWidth, y), (sWidth, y))

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
