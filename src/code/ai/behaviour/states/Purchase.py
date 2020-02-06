import random

from src.code.ai.behaviour.IState import IState
from src.code.engine.GameTime import GameTime
from src.code.environment.AllBuildings import getStore
from ...messaging.Message import Message


class Purchase(IState):

    def __init__(self):
        alternatives = ["Shovel", "Pair of glasses", "Banana", "Skateboard", "Teddy bear", "Programming Game AI by Example, Mat Buckland"]
        selection = random.randrange(0, len(alternatives))
        self.item = alternatives[selection]
        self.startTime = GameTime.ticks

    def __repr__(self):
        return 'Purchasing'

    def enter(self, entity):
        Message.sendConsole(entity, "Time to make use of my funds, I'll get myself a " + self.item)

    def execute(self, entity):

        if not entity.isCloseTo(getStore().position):
            entity.moveTo(getStore().position)
            return

        if entity.bank <= 5:
            from .Sleep import Sleep
            entity.setState(Sleep())

        elif GameTime.ticks - self.startTime >= GameTime.minutesToMilliseconds(0.20):
            from .Hangout import Hangout
            entity.setState(Hangout())

        entity.bank -= 3 * GameTime.deltaTime
        entity.hunger += 1 * GameTime.deltaTime

    def exit(self, entity):
        pass
