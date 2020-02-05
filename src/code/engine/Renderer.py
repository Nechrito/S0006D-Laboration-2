import pygame
import pygame.freetype
from src.Settings import *
from src.code.engine import Map


class Renderer:

    def __init__(self, surface):
        self.surface = surface
        self.texts = []

    def clear(self):
        pygame.display.update()

    def renderTile(self, image, position):
        self.surface.blit(image, (position[0], position[1]))

    def renderCircle(self, position, radius, color=(255, 255, 255)):
        pygame.draw.circle(self.surface, color, position, radius, 1)

    def renderRect(self, size, pos, color=(255, 255, 255), alpha=128):
        rect = pygame.Surface(size)
        rect.set_alpha(alpha)
        rect.fill(color)
        self.surface.blit(rect, pos)

    def renderRect2(self, rect, color=(255, 255, 255), alpha=128):
        self.renderRect((rect[2], rect[3]), (rect[0], rect[1]), color, alpha)

    def renderRectIntersection(self, rectangles, collisionPoint):
        for i in range(len(rectangles)):
            rect = rectangles[i]
            if rect.collidepoint((collisionPoint[0] + TILESIZE / 2, collisionPoint[1] + TILESIZE / 2)):
                rectSurface = pygame.Surface((TILESIZE, TILESIZE))
                rectSurface.set_alpha(255)
                rectSurface.fill((171, 255, 212))
                self.surface.blit(rectSurface, (rect[0], rect[1]))
                break

    def renderGrid(self):
        color = (171, 255, 212)
        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pygame.draw.line(self.surface, color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pygame.draw.line(self.surface, color, (0, y), (SCREEN_WIDTH, y))

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
