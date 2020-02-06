from datetime import datetime

import pygame
import datetime


class GameTime:

    timeScale = 1
    ticks = 0
    totalTicks = 0

    lastFrame = 0
    deltaTime = 0
    fixedDeltaTime = 0

    startDate: datetime

    @classmethod
    def init(cls):
        cls.startDate = datetime.datetime.now()

    @classmethod
    def setScale(cls, scale):
        cls.timeScale = scale
        return cls.timeScale

    @classmethod
    def updateTicks(cls):
        cls.ticks = pygame.time.get_ticks()

        cls.deltaTime = cls.fixedDeltaTime = ((cls.ticks - cls.lastFrame) / 1000.0)
        cls.deltaTime *= cls.timeScale  # post multiplying only here prevents fixedDeltaTime from scaling

        cls.lastFrame = cls.ticks

    @classmethod
    def timeElapsed(cls):
        increment = datetime.timedelta(milliseconds=(cls.ticks * cls.timeScale) * 100)
        return (datetime.datetime.now() + increment).strftime("%d/%m-%y %H:%M")

    @classmethod
    def minutesToMilliseconds(cls, minute):
        return (minute * 60000) / cls.timeScale
