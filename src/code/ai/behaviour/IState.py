import abc

from src.code.engine.Entity import Entity


class IState(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def enter(self, entity: Entity):
        pass

    @abc.abstractmethod
    def execute(self, entity: Entity):
        pass

    @abc.abstractmethod
    def exit(self, entity: Entity):
        pass


