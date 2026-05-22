"""Application profile detection and gesture mappings."""
from dataclasses import dataclass
import os
import platform
import subprocess

from desktop_control_prototype.intents import Intent
from desktop_control_prototype.state_machine import Mode


@dataclass(frozen=True)
class AppProfile:
    name: str
    keywords: tuple[str, ...]


PROFILES = (
    AppProfile(name="Explorer", keywords=("file explorer", "explorer", "files")),
    AppProfile(name="Word", keywords=("microsoft word", "word")),
)


def detect_active_window_title():
    override = os.environ.get("MMDC_ACTIVE_WINDOW_TITLE", "").strip()
    if override:
        return override

    try:
        import pygetwindow as gw  # type: ignore

        window = gw.getActiveWindow()
        if window and getattr(window, "title", None):
            return window.title
    except Exception:
        pass

    if platform.system() == "Linux":
        # Prefer xdotool to get the active window name
        try:
            completed = subprocess.run(("xdotool", "getactivewindow", "getwindowname"), capture_output=True, text=True, check=False)
            text = completed.stdout.strip()
            if text:
                return text.splitlines()[0]
        except Exception:
            pass

        # If xdotool is available, get the active window PID and resolve the process name
        try:
            completed = subprocess.run(("xdotool", "getactivewindow", "getwindowpid"), capture_output=True, text=True, check=False)
            pid_text = completed.stdout.strip()
            if pid_text.isdigit():
                pid = int(pid_text)
                proc = subprocess.run(("ps", "-p", str(pid), "-o", "comm="), capture_output=True, text=True, check=False)
                proc_name = proc.stdout.strip().lower()
                if proc_name:
                    return proc_name
        except Exception:
            pass

        # As a last resort, try wmctrl and return the first non-empty line
        try:
            completed = subprocess.run(("wmctrl", "-lp"), capture_output=True, text=True, check=False)
            text = completed.stdout.strip()
            if text:
                return text.splitlines()[0]
        except Exception:
            pass

    return ""


def detect_active_profile(window_title=None):
    title = (window_title if window_title is not None else detect_active_window_title()).lower()
    for profile in PROFILES:
        if any(keyword in title for keyword in profile.keywords):
            return profile.name
    return "Generic"


def resolve_profile_intent(profile_name, mode, gesture):
    if profile_name == "Explorer":
        if mode == Mode.IDLE.name and gesture == "Open_Palm":
            return Intent(gesture=gesture, action="enter_navigation_mode", next_mode=Mode.EXPLORER_NAV.name)
        if mode == Mode.EXPLORER_NAV.name and gesture == "Open_Palm":
            return Intent(gesture=gesture, action="navigate_down", next_mode=None)
        if mode == Mode.EXPLORER_NAV.name and gesture == "Pinch":
            return Intent(gesture=gesture, action="open_selected_item", next_mode=None)
        if mode == Mode.EXPLORER_NAV.name and gesture == "Pointing":
            return Intent(gesture=gesture, action="focus_address_bar", next_mode=None)
        if mode == Mode.EXPLORER_NAV.name and gesture == "Closed_Fist":
            return Intent(gesture=gesture, action="go_back", next_mode=None)

    if profile_name == "Word":
        if mode == Mode.IDLE.name and gesture == "Open_Palm":
            return Intent(gesture=gesture, action="enter_app_control_mode", next_mode=Mode.APP_CONTROL.name)
        if mode == Mode.APP_CONTROL.name and gesture == "Pinch":
            return Intent(gesture=gesture, action="save_document", next_mode=None)
        if mode == Mode.APP_CONTROL.name and gesture == "Open_Palm":
            return Intent(gesture=gesture, action="find", next_mode=None)
        if mode == Mode.APP_CONTROL.name and gesture == "Pointing":
            return Intent(gesture=gesture, action="select_all", next_mode=None)
        if mode == Mode.APP_CONTROL.name and gesture == "Closed_Fist":
            return Intent(gesture=gesture, action="bold", next_mode=None)

    return None