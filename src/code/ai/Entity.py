import math
import time
from typing import List, Any

import pygame
from src.code.ai.fsm.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
import random

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.PathManager import PathManager, getFullPath
from src.enums.PathType import PathType


class Entity(pygame.sprite.Sprite):

    waypoints: List[Node]

    def __init__(self, name, state, globalState, group, image, position: vec2):

        pygame.sprite.Sprite.__init__(self, group)
        self.image = image
        self.name = name
        self.position = position
        self.waypoints = []

        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.X
        self.rect.centery = self.position.Y

        self.pathfinder = PathManager(0)
        self.nextNode = self.position
        self.radius = 2

        self.fatigue = random.randrange(0, 70)
        self.bank = random.randrange(0, 120)
        self.thirst = random.randrange(0, 50)
        self.hunger = random.randrange(0, 50)

        #self.stateMachine = StateMachine(self, state, globalState)

    def updateState(self):
        self.thirst += 0.5 * GameTime.deltaTime
        self.hunger += 0.5 * GameTime.deltaTime
        self.fatigue += 0.5 * GameTime.deltaTime
        #self.stateMachine.update()

    def update(self):
        if len(self.waypoints) <= 1:
            return

        if self.nextNode.distance(self.position) > self.radius or self.waypoints[-1].position == self.nextNode:
            self.position += (self.nextNode - self.position).normalized * GameTime.deltaTime * 200

            self.rect = self.image.get_rect()
            self.rect.topleft = self.position.tuple

            self.rect.centerx = self.position.X
            self.rect.centery = self.position.Y

        elif len(self.waypoints) >= 2:
            self.waypoints = self.pathfinder.cutPath(self, self.waypoints)
            if len(self.waypoints) >= 2:
                self.nextNode = self.waypoints[1].position

    def setPath(self, waypoints):
        temp = self.pathfinder.requestPath(self.position, waypoints[0].position)
        temp.extend(waypoints)
        self.waypoints = temp
        self.nextNode = self.waypoints[1].position

    def moveTo(self, node: vec2):
        if len(self.waypoints) >= 1:
            self.pathfinder.requestPathCached(self.waypoints, self, node)

    def setState(self, state, lock=False):
        # self.stateMachine.setLockedState(lock)
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()

    def isCloseTo(self, to: vec2):
        return self.position.distance(to) <= self.radius
