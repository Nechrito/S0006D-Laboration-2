import pygame
from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.engine.GameTime import GameTime


class CameraInstance:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.X = 0
        self.Y = 0
        self.width = width
        self.height = height

    def moveRect(self, rect):
        return rect.move(self.camera.topleft)

    def moveSprite(self, entity):
        return entity.rect.move(self.camera.topleft)

    def followTarget(self, target: Entity):

        self.x += ((-target.rect.centerx + int(SETTINGS.SCREEN_WIDTH / 2)) - self.X) * GameTime.fixedDeltaTime
        self.y += ((-target.rect.centery + int(SETTINGS.SCREEN_HEIGHT / 2)) - self.Y) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        self.x = min(0, self.X)
        self.y = min(0, self.Y)
        self.x = max(-(self.width - SETTINGS.SCREEN_WIDTH), self.X)
        self.y = max(-(self.height - SETTINGS.SCREEN_HEIGHT), self.Y)

        self.camera = pygame.Rect(self.X, self.Y, self.width, self.height)
