import pygame
from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.engine.GameTime import GameTime


class CameraInstance:
    center: vec2
    rect: pygame.Rect
    width: int
    height: int

    @classmethod
    def init(cls, width, height):
        cls.center = vec2(0, 0)
        cls.rect = pygame.Rect(0, 0, width, height)
        cls.width = width
        cls.height = height

    @classmethod
    def centeredRect(cls, rect):
        return rect.copy().move(cls.rect.topleft)

    @classmethod
    def centeredSprite(cls, sprite):
        return sprite.rect.copy().move(cls.rect.topleft)

    @classmethod
    def centeredVec(cls, vec):
        #camPos = vec2(CameraInstance.center.X, CameraInstance.center.Y)
        #camPos = vec2(0, 0)
        #return (camPos + vec).tuple
        return vec2(vec[0], vec[1]).tuple

    @classmethod
    def followTarget(cls, target: Entity):

        centerx = (-target.rect.centerx + SETTINGS.SCREEN_WIDTH // 2) - cls.center.X
        centery = (-target.rect.centery + SETTINGS.SCREEN_HEIGHT // 2) - cls.center.Y

        cls.center += vec2(centerx, centery) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        xMin = min(0, cls.center.X)
        yMin = min(0, cls.center.Y)

        xMax = max(-(cls.width - SETTINGS.SCREEN_WIDTH), xMin)
        yMax = max(-(cls.height - SETTINGS.SCREEN_HEIGHT), yMin)

        cls.center = vec2(xMax, yMax)
        cls.rect = pygame.Rect(cls.center.X, cls.center.Y, cls.width, cls.height)
