import pygame
from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.engine.GameTime import GameTime
from src.code.math.Vector import vec2


class CameraInstance:
    center: vec2
    rect: pygame.Rect
    width: int
    height: int

    @classmethod
    def init(cls):
        cls.center = vec2()
        print(str(SETTINGS.MAP_WIDTH))
        cls.rect = pygame.Rect(0, 0, SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT)
        cls.width = cls.rect[2]
        cls.height = cls.rect[3]

    @classmethod
    def centeredRect(cls, rect):
        return rect.move(cls.rect.topleft)

    @classmethod
    def centeredSprite(cls, sprite):
        return sprite.rect.move(cls.rect.topleft)

    @classmethod
    def centeredVec(cls, vec):
        if SETTINGS.CURRENT_LEVEL >= 4:
            camPos = vec2(CameraInstance.center.X, CameraInstance.center.Y)
            return (camPos + vec).tuple
        else:
            return vec[0], vec[1]

    @classmethod
    def followTarget(cls, target: Entity):

        centerx = (-target.position.X + cls.width // 2) - cls.center.X
        centery = (-target.position.Y + cls.height // 2) - cls.center.Y

        cls.center += vec2(centerx, centery) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        xMin = min(0, cls.center.X)
        yMin = min(0, cls.center.Y)

        xMax = max(-(cls.width - SETTINGS.SCREEN_WIDTH), xMin)
        yMax = max(-(cls.height - SETTINGS.SCREEN_HEIGHT), yMin)

        cls.center = vec2(xMax, yMax)
        cls.rect = pygame.Rect(cls.center.X, cls.center.Y, cls.width, cls.height)
