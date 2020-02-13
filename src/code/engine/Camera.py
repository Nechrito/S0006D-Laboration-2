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
        cls.center = vec2((width / 2) * SETTINGS.TILE_SCALE[0], (height / 2) * SETTINGS.TILE_SCALE[1])
        cls.rect = pygame.Rect(cls.center.X, cls.center.Y, SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1])
        cls.width = width
        cls.height = height

    @classmethod
    def centeredRect(cls, rect):
        return rect.move(cls.rect.topleft)

    @classmethod
    def centeredSprite(cls, sprite):
        return sprite.rect.move(cls.rect.topleft)

    @classmethod
    def centeredVec(cls, vec):
        if SETTINGS.MAP_LEVEL >= 4:
            camPos = vec2(CameraInstance.center.X, CameraInstance.center.Y)
            return (camPos + vec).tuple
        else:
            return vec2(vec[0], vec[1]).tuple

    @classmethod
    def followTarget(cls, target: Entity):

        centerx = (-target.position.X + SETTINGS.SCREEN_WIDTH // 2) - cls.center.X
        centery = (-target.position.Y + SETTINGS.SCREEN_HEIGHT // 2) - cls.center.Y

        cls.center += vec2(centerx, centery) * GameTime.fixedDeltaTime

        #  Make sure we're within map boundaries
        xMin = min(0, cls.center.X)
        yMin = min(0, cls.center.Y)

        xMax = max(-(cls.width - SETTINGS.SCREEN_WIDTH), xMin)
        yMax = max(-(cls.height - SETTINGS.SCREEN_HEIGHT), yMin)

        cls.center = vec2(xMax, yMax)
        cls.rect = pygame.Rect(cls.center.X, cls.center.Y, cls.width, cls.height)
