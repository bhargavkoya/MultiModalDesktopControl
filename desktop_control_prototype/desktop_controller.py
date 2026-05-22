"""Desktop automation wrappers (stubs for now)."""
try:
    import pyautogui
except Exception:
    pyautogui = None


class DesktopController:
    def click(self):
        if pyautogui:
            pyautogui.click()
        else:
            print("pyautogui not available: click simulated")
