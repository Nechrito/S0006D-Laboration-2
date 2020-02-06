import pygame
from src.Settings import *
from src.code.engine.Entity import Entity
from src.code.engine.GameTime import GameTime


class CameraInstance:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def moveRect(self, rect):
        return rect.move(self.camera.topleft)

    def moveSprite(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target: Entity):

        self.x += ((-target.rect.centerx + int(SCREEN_WIDTH / 2)) - self.x) * GameTime.fixedDeltaTime
        self.y += ((-target.rect.centery + int(SCREEN_HEIGHT / 2)) - self.y) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        self.x = min(0, self.x)
        self.y = min(0, self.y)
        self.x = max(-(self.width - SCREEN_WIDTH), self.x)
        self.y = max(-(self.height - SCREEN_HEIGHT), self.y)

        self.camera = pygame.Rect(self.x, self.y, self.width, self.height)
