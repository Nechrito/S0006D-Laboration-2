from ..IState import IState
from ...messaging.Message import Message
from ....engine.GameTime import GameTime
from ....environment.AllBuildings import getDrink


class Drink(IState):

    def __repr__(self):
        return 'Drinking'

    def enter(self, entity):
        Message.sendConsole(entity, "Need me a beverage")

    def execute(self, entity):

        if not entity.isCloseTo(getDrink().position):
            entity.moveTo(getDrink().position)
            return

        if entity.thirst <= 5:
            entity.revertState()
        else:
            entity.thirst -= 5 * GameTime.deltaTime
            entity.bank -= 0.30 * GameTime.deltaTime

    def exit(self, entity):
        pass
