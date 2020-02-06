from src.code.ai.behaviour.IState import IState


class StateTransition:
    def __init__(self, currentState: IState, nextState: IState) -> IState:
        self.currentState = currentState
        self.nextState = nextState

    def __eq__(self, other):
        return isinstance(other, StateTransition) \
               and self.currentState == other.currentState \
               and self.nextState == other.nextState

    def __hash__(self):
        return hash(self.currentState) + hash(self.nextState)

    def toString(self):
        return "Current: " + str(self.currentState) + " Next: " + str(self.nextState)