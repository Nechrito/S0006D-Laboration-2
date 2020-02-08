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
        rect = pygame.Surface(size)
        rect.set_alpha(alpha)
        rect.fill(color)
        self.surface.blit(rect, pos)

    def renderRect2(self, rect, color=(255, 255, 255), alpha=128):
        self.renderRect((rect[2], rect[3]), (rect[0], rect[1]), color, alpha)

    def renderRectIntersection(self, rectangles, collisionPoint):
        for rect in rectangles:

            if rect.collidepoint((collisionPoint[0] + SETTINGS.TILE_WIDTH / 2, collisionPoint[1] + SETTINGS.TILE_HEIGHT / 2)):
                rectSurface = pygame.Surface((SETTINGS.TILE_WIDTH, SETTINGS.TILE_HEIGHT))
                rectSurface.set_alpha(255)
                rectSurface.fill((171, 255, 212))
                self.surface.blit(rectSurface, (rect[0], rect[1]))
                break

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
