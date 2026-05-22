"""Gesture-to-intent mapping for the prototype.

This layer keeps gesture classification separate from desktop actions so it can
be extended later with more states, cooldowns, and app-specific profiles.
"""
from dataclasses import dataclass

from desktop_control_prototype.config import PINCH_THRESHOLD
from desktop_control_prototype.state_machine import Mode


@dataclass(frozen=True)
class Intent:
    gesture: str
    action: str
    next_mode: str | None = None


def classify_pose(landmarks):
    """Classify a landmark list into a coarse hand pose label.

    Returns one of: None, Pointing, Open_Palm, Closed_Fist, Pinch, Unknown.
    """
    if not landmarks:
        return "None"

    try:
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
    except (IndexError, TypeError):
        return "Unknown"

    pinch_distance = abs(index_tip[0] - thumb_tip[0]) + abs(index_tip[1] - thumb_tip[1])
    if pinch_distance < PINCH_THRESHOLD:
        return "Pinch"

    index_extended = index_tip[1] < index_pip[1]
    middle_extended = middle_tip[1] < middle_pip[1]
    ring_extended = ring_tip[1] < ring_pip[1]
    pinky_extended = pinky_tip[1] < pinky_pip[1]

    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "Pointing"

    if index_extended and middle_extended and ring_extended and pinky_extended:
        return "Open_Palm"

    if not index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "Closed_Fist"

    return "Unknown"


def resolve_intent(mode, gesture):
    """Translate current mode and gesture into a symbolic intent."""
    if gesture == "None":
        return Intent(gesture=gesture, action="idle", next_mode=None)

    if mode == Mode.IDLE.name:
        if gesture == "Pointing":
            return Intent(gesture=gesture, action="enter_pointer_mode", next_mode=Mode.POINTER.name)
        if gesture == "Open_Palm":
            return Intent(gesture=gesture, action="enter_navigation_mode", next_mode=Mode.EXPLORER_NAV.name)
        if gesture == "Closed_Fist":
            return Intent(gesture=gesture, action="pause", next_mode=Mode.PAUSED.name)

    if mode == Mode.POINTER.name:
        if gesture == "Pinch":
            return Intent(gesture=gesture, action="pointer_pinch", next_mode=None)
        if gesture == "Closed_Fist":
            return Intent(gesture=gesture, action="pause", next_mode=Mode.PAUSED.name)

    if mode == Mode.EXPLORER_NAV.name:
        if gesture == "Open_Palm":
            return Intent(gesture=gesture, action="navigate_down", next_mode=None)
        if gesture == "Pinch":
            return Intent(gesture=gesture, action="open_selected_item", next_mode=None)

    if mode == Mode.PAUSED.name and gesture == "Open_Palm":
        return Intent(gesture=gesture, action="resume", next_mode=Mode.IDLE.name)

    return Intent(gesture=gesture, action="no_op", next_mode=None)
