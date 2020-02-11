import pygame
from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.engine.GameTime import GameTime


class CameraInstance:

    def __init__(self, width, height):
        self.center = vec2(0, 0)
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def centered(self, rect):
        return rect.move(self.rect.topleft)

    def followTarget(self, target: Entity):

        centerx = (-target.position.X + int(SETTINGS.SCREEN_WIDTH // 2)) - self.center.X
        centery = (-target.position.Y + int(SETTINGS.SCREEN_HEIGHT // 2)) - self.center.Y

        self.center += vec2(centerx, centery) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        xMin = min(0, self.center.X)
        yMin = min(0, self.center.Y)

        xMax = max(-(self.width - SETTINGS.SCREEN_WIDTH), xMin)
        yMax = max(-(self.height - SETTINGS.SCREEN_HEIGHT), yMin)

        self.center = vec2(xMax, yMax)
        self.rect = pygame.Rect(self.center.X, self.center.Y, self.width, self.height)
