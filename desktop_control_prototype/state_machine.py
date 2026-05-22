"""Simple state machine for modes defined in PRD."""
from enum import Enum, auto


class Mode(Enum):
    IDLE = auto()
    POINTER = auto()
    COMMAND = auto()
    LAUNCHER = auto()
    EXPLORER_NAV = auto()
    APP_CONTROL = auto()
    PAUSED = auto()


class StateMachine:
    def __init__(self):
        self.state = Mode.IDLE

    def transition(self, new_state):
        # Accept either a Mode enum or a mode name string.
        if isinstance(new_state, Mode):
            self.state = new_state
            return

        if isinstance(new_state, str):
            self.state = Mode[new_state]
            return

        raise TypeError(f"Unsupported state type: {type(new_state)!r}")

    def get_state(self):
        return self.state.name
