"""Simple local command adapter that maps short text commands to Intents.

This is intentionally small and offline-friendly: it's a mapping helper
useful for testing and for wiring a later LLM layer.
"""
from desktop_control_prototype.intents import Intent
from desktop_control_prototype.state_machine import Mode


def parse_command(text, current_mode: str | None = None) -> Intent | None:
    if not text:
        return None
    t = text.strip().lower()

    if t in ("open explorer", "open file explorer", "show explorer", "explorer"):
        return Intent(gesture="command", action="enter_navigation_mode", next_mode=Mode.EXPLORER_NAV.name)
    if t in ("pointer mode", "enter pointer mode", "pointing mode", "pointer"):
        return Intent(gesture="command", action="enter_pointer_mode", next_mode=Mode.POINTER.name)
    if t in ("save", "save document", "save file"):
        return Intent(gesture="command", action="save_document", next_mode=None)
    if t in ("find", "search"):
        return Intent(gesture="command", action="find", next_mode=None)
    if t in ("select all", "selectall"):
        return Intent(gesture="command", action="select_all", next_mode=None)
    if t in ("bold", "make bold"):
        return Intent(gesture="command", action="bold", next_mode=None)
    if t in ("go back", "back"):
        return Intent(gesture="command", action="go_back", next_mode=None)
    if t in ("address bar", "focus address bar", "focus url"):
        return Intent(gesture="command", action="focus_address_bar", next_mode=None)
    if t in ("click", "left click"):
        return Intent(gesture="command", action="click", next_mode=None)

    return None
