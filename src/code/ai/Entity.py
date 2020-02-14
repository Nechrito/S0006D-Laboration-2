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

        if SETTINGS.CURRENT_LEVEL >= 4 and state is not None:
            self.stateMachine = StateMachine(self, state, globalState)
        else:
            self.stateMachine = None

    def updateState(self):
        self.thirst += 0.5 * GameTime.deltaTime
        self.hunger += 0.5 * GameTime.deltaTime
        self.fatigue += 0.5 * GameTime.deltaTime
        self.stateMachine.update()

    def update(self):
        if SETTINGS.CURRENT_LEVEL >= 4 and self.stateMachine is not None:
            self.updateState()

        if len(self.waypoints) <= 1:
            return

        if self.nextNode.distance(self.position) > self.radius:
            self.position += (self.nextNode - self.position).normalized * GameTime.deltaTime * 200
        elif len(self.waypoints) >= 2:
            self.waypoints = self.pathfinder.cutPath(self, self.waypoints)
            if len(self.waypoints) >= 2:
                self.nextNode = self.waypoints[1].position

    def moveTo(self, target: vec2):
        if target.distance(self.position) <= self.radius:
            return

        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, target)
        if temp is None:
            return

        self.waypoints = temp
        self.nextNode = self.waypoints[1].position

    def setStart(self, start: vec2, end: vec2 = None):
        self.waypoints = []
        #path = self.pathfinder.requestPath(SETTINGS.closestTile(self.position).position, start)
        #if path is None:
            #return

        temp = self.pathfinder.requestPath(start, end)
        if temp is None:
            return

        #temp.append(path)
        self.position = start
        self.waypoints = temp
        self.nextNode = self.waypoints[1].position

    def setState(self, state, lock=False):
        # self.stateMachine.setLockedState(lock)
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()

    def isCloseTo(self, to: vec2):
        return self.position.distance(to) <= self.radius
