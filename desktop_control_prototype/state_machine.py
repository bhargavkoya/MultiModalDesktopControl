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
        # Add simple gating rules here if needed
        self.state = new_state

    def get_state(self):
        return self.state.name
