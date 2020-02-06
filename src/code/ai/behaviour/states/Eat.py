from ..IState import IState
from ....engine.GameTime import GameTime
from ....environment.AllBuildings import getResturant
from ...messaging.Message import Message


class Eat(IState):

    def __repr__(self):
        return 'Eating'

    def enter(self, entity):
        Message.sendConsole(entity, "Time to get myself a snack!")

    def execute(self, entity):

        if not entity.isCloseTo(getResturant().position):
            entity.moveTo(getResturant().position)
            return

        if entity.hunger <= 5 or entity.bank <= 2:
            from .CollectMoney import CollectMoney
            entity.setState(CollectMoney())
        else:
            entity.hunger -= 4 * GameTime.deltaTime
            entity.bank -= 0.40 * GameTime.deltaTime

    def exit(self, entity):
        pass
