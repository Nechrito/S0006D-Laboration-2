class StateMachine:

    def __init__(self, entity, currentstate, globalState):
        self.owner = entity
        self.globalState = globalState
        self.locked = False
        self.previousState = None
        self.currentState = currentstate
        self.currentState.enter(self.owner)

    def update(self):
        if not self.locked:
            self.currentState.execute(self.owner)

        self.globalState.execute(self.owner)

    def setLockedState(self, value):
        self.locked = value

    def revert(self):
        if self.previousState is not None:
            self.change(self.previousState)

    def change(self, nextState):

        if self.locked:
            return

        self.previousState = self.currentState

        self.currentState.exit(self.owner)

        self.currentState = nextState

        self.currentState.enter(self.owner)
