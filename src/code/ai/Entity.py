from typing import List

from src.Settings import *
from src.code.ai.fsm.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
import random

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.PathManager import PathManager
from src.enums.PathType import PathType


class Entity:

    waypoints: List[Node]

    def __init__(self, name, state, globalState, image, position: vec2):
        self.image = image
        self.name = name
        self.position = position
        self.waypoints = []

        self.pathfinder = PathManager(PathType.AStar)
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
        if not self.waypoints or len(self.waypoints) <= 1:
            return

        if self.nextNode.distance(self.position) > self.radius:
            self.position += (self.nextNode - self.position).normalized * GameTime.deltaTime * 200
        elif len(self.waypoints) >= 2:
            self.waypoints = self.pathfinder.cutPath(self, self.waypoints)
            if len(self.waypoints) >= 2:
                self.nextNode = self.waypoints[1].position

    def moveTo(self, target: vec2):
        if not target:
            return

        if target.distance(self.position) <= self.radius:
            return

        self.waypoints = self.pathfinder.requestPathCached(self.waypoints, self.position, target)

    def setStart(self, start: vec2, end: vec2 = None):
        self.position = start
        if end:
            self.waypoints = self.pathfinder.requestPath(start, end)
            if self.waypoints and len(self.waypoints) >= 2:
                self.nextNode = self.waypoints[1].position

    def setState(self, state, lock=False):
        # self.stateMachine.setLockedState(lock)
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()

    def isCloseTo(self, to: vec2):
        return self.position.distance(to) <= self.radius
