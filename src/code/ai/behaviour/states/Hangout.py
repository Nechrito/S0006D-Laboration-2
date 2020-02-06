from src.code.ai.behaviour.IState import IState
from src.code.engine.GameTime import GameTime
from src.code.environment.AllBuildings import getHangout
from src.code.ai.messaging.Message import Message


class Hangout(IState):

    def __repr__(self):
        return 'Hangout'

    def enter(self, entity):
        Message.sendConsole(entity, "Can't wait to hangout with my pals")

    def execute(self, entity):
        if not entity.isCloseTo(getHangout().position):
            entity.moveTo(getHangout().position)
            return

        if entity.fatigue > 80 or entity.bank <= 5:
            from .Sleep import Sleep
            entity.setState(Sleep())
        else:
            entity.bank -= 1.5 * GameTime.deltaTime
            entity.fatigue += 1 * GameTime.deltaTime

    def exit(self, entity):
        pass
