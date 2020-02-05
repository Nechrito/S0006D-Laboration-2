import math

import pygame
from src.Settings import *
from src.code.ai.fsm.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
import random


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, state, globalState, category, x, y, image):

        pygame.sprite.Sprite.__init__(self, category)

        self.image = image
        self.name = name
        self.position = [x + TILE_SIZE / 2, y + TILE_SIZE / 2]
        self.length = 0
        self.limit = 0
        self.direction = [0, 0]

        self.fatigue = random.randrange(0, 70)
        self.bank = random.randrange(0, 120)
        self.thirst = random.randrange(0, 50)
        self.hunger = random.randrange(0, 50)

        self.stateMachine = StateMachine(self, state, globalState)

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        self.thirst += 0.5 * GameTime.deltaTime
        self.hunger += 0.5 * GameTime.deltaTime
        self.fatigue += 0.5 * GameTime.deltaTime

        self.stateMachine.update()

    def isClose(self, distance=20):
        return self.length <= distance

    def isCloseTo(self, target, distance=20):
        return self.distanceTo(target) <= distance

    def distanceTo(self, target):
        return math.sqrt((self.position[0] - target[0]) ** 2 + (self.position[1] - target[1]) ** 2)

    def moveTo(self, target, limit = 0):
        length = self.distanceTo(target)

        self.length = length
        self.limit = limit

        self.direction[0] = ((target[0] - self.position[0]) / self.length)
        self.direction[1] = ((target[1] - self.position[1]) / self.length)

        self.position[0] += self.direction[0] * GameTime.deltaTime * 30
        self.position[1] += self.direction[1] * GameTime.deltaTime * 30

    def setState(self, state, lock=False):
        # self.stateMachine.setLockedState(lock)
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()
