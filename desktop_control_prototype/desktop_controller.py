"""Desktop automation wrappers (stubs for now)."""
try:
    import pyautogui
except Exception:
    pyautogui = None

from desktop_control_prototype.config import DEFAULT_SCREEN_HEIGHT, DEFAULT_SCREEN_WIDTH
from desktop_control_prototype.shortcuts import BOLD, FIND, SAVE_DOCUMENT, SELECT_ALL


class DesktopController:
    def __init__(self):
        if pyautogui is not None:
            pyautogui.FAILSAFE = True

    def click(self):
        if pyautogui:
            pyautogui.click()
        else:
            print("pyautogui not available: click simulated")

    def mouse_down(self, button="left"):
        if pyautogui:
            pyautogui.mouseDown(button=button)
        else:
            print(f"pyautogui not available: mouseDown({button}) simulated")

    def mouse_up(self, button="left"):
        if pyautogui:
            pyautogui.mouseUp(button=button)
        else:
            print(f"pyautogui not available: mouseUp({button}) simulated")

    def hotkey(self, *keys):
        if pyautogui:
            pyautogui.hotkey(*keys)
        else:
            print(f"pyautogui not available: hotkey {keys} simulated")

    def press(self, key):
        if pyautogui:
            pyautogui.press(key)
        else:
            print(f"pyautogui not available: press {key} simulated")

    def scroll(self, clicks):
        if pyautogui:
            pyautogui.scroll(clicks)
        else:
            print(f"pyautogui not available: scroll {clicks} simulated")

    def move_to(self, x, y, duration=0):
        if pyautogui:
            pyautogui.moveTo(x, y, duration=duration)
        else:
            print(f"pyautogui not available: moveTo({x}, {y}) simulated")

    def drag_to(self, x, y, duration=0, button="left"):
        if pyautogui:
            pyautogui.dragTo(x, y, duration=duration, button=button)
        else:
            print(f"pyautogui not available: dragTo({x}, {y}) simulated")

    def screen_size(self):
        if pyautogui:
            return pyautogui.size()
        return DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT

    def move_pointer_normalized(self, x_norm, y_norm, duration=0):
        width, height = self.screen_size()
        x = max(0, min(width - 1, int(x_norm * width)))
        y = max(0, min(height - 1, int(y_norm * height)))
        self.move_to(x, y, duration=duration)

    def open_explorer(self):
        self.hotkey("win", "e")

    def go_back(self):
        self.press("backspace")

    def focus_address_bar(self):
        self.hotkey("ctrl", "l")

    def open_selected(self):
        self.press("enter")

    def navigate_up(self):
        self.press("up")

    def navigate_down(self):
        self.press("down")

    def save_document(self):
        self.hotkey(*SAVE_DOCUMENT)

    def find(self):
        self.hotkey(*FIND)

    def select_all(self):
        self.hotkey(*SELECT_ALL)

    def bold(self):
        self.hotkey(*BOLD)

    def pause(self):
        print("Prototype paused")

    def resume(self):
        print("Prototype resumed")
