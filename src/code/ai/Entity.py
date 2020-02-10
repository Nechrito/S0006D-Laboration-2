import math
import time

import pygame
from src.code.ai.fsm.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
import random

from src.code.math.Vector import vec2
from src.code.pathfinding.PathManager import PathManager


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, state, globalState, category, image, position: vec2):

        pygame.sprite.Sprite.__init__(self, category)

        self.image = image
        self.name = name
        self.position = position

        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.X
        self.rect.centery = self.position.Y

        self.pathfinder = PathManager()
        self.nextNode = self.position
        self.radius = 10
        self.waypoints = []

        self.fatigue = random.randrange(0, 70)
        self.bank = random.randrange(0, 120)
        self.thirst = random.randrange(0, 50)
        self.hunger = random.randrange(0, 50)

        self.stateMachine = StateMachine(self, state, globalState)

    def updateState(self):
        self.thirst += 0.5 * GameTime.deltaTime
        self.hunger += 0.5 * GameTime.deltaTime
        self.fatigue += 0.5 * GameTime.deltaTime
        self.stateMachine.update()

    def update(self):
        self.pathfinder.update(self)

        if self.nextNode.distance(self.position) >= self.radius:
            self.position += (self.nextNode - self.position).normalized * GameTime.deltaTime * 200
        else:
            self.waypoints.pop()
            if self.waypoints:
                self.nextNode = self.waypoints[0].position

        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.X
        self.rect.centery = self.position.Y

    def setPath(self, waypoints):
        self.waypoints = waypoints
        self.pathfinder.path = self.waypoints
        self.nextNode = self.waypoints[0].position

    def moveTo(self, node: vec2):
        self.waypoints = self.pathfinder.requestPathCached(self, node)

    def setState(self, state, lock=False):
        # self.stateMachine.setLockedState(lock)
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()

    def isCloseTo(self, to: vec2):
        return self.position.distance(to) <= self.radius
