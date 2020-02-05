import pygame
import pygame.freetype
from src.Settings import *


class Renderer:

    def __init__(self, surface):
        self.surface = surface
        self.texts = []

    def clear(self, mapImg, mapRect):
        pygame.display.update()
        self.surface.blit(mapImg, mapRect)

    def renderCircle(self, position, radius, color=(255, 255, 255)):
        pygame.draw.circle(self.surface, color, position, radius, 1)

    def renderRect(self, size, pos, color=(255, 255, 255), alpha=128):
        rect = pygame.Surface(size)
        rect.set_alpha(alpha)
        rect.fill(color)
        self.surface.blit(rect, pos)

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