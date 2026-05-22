"""Pointer gesture timing helpers."""

from dataclasses import dataclass

from desktop_control_prototype.config import DRAG_HOLD_SECONDS


@dataclass
class PointerGestureState:
    pinch_started_at: float | None = None
    dragging: bool = False

    def reset(self):
        self.pinch_started_at = None
        self.dragging = False


def advance_pointer_gesture(pointer_state, gesture, now):
    if gesture == "Pinch":
        if pointer_state.pinch_started_at is None:
            pointer_state.pinch_started_at = now

        elapsed = now - pointer_state.pinch_started_at
        if not pointer_state.dragging and elapsed >= DRAG_HOLD_SECONDS:
            pointer_state.dragging = True
            return "drag_start"
        if pointer_state.dragging:
            return "drag_update"
        return "hold_pending"

    if pointer_state.pinch_started_at is None:
        return None

    elapsed = now - pointer_state.pinch_started_at
    was_dragging = pointer_state.dragging
    pointer_state.reset()

    if was_dragging:
        return "drag_end"
    if elapsed >= DRAG_HOLD_SECONDS:
        return "drag_tap"
    return "click"