"""Prototype thresholds and runtime tuning values."""

import os

POINTER_SMOOTHING = 0.7
PINCH_THRESHOLD = 0.08
ACTION_COOLDOWN_SECONDS = 0.25
DRAG_HOLD_SECONDS = 0.35
DEFAULT_SCREEN_WIDTH = 1920
DEFAULT_SCREEN_HEIGHT = 1080
POINTER_X_MIN = float(os.environ.get("MMDC_POINTER_X_MIN", "0.05"))
POINTER_X_MAX = float(os.environ.get("MMDC_POINTER_X_MAX", "0.95"))
POINTER_Y_MIN = float(os.environ.get("MMDC_POINTER_Y_MIN", "0.08"))
POINTER_Y_MAX = float(os.environ.get("MMDC_POINTER_Y_MAX", "0.92"))
POINTER_FLIP_X = os.environ.get("MMDC_POINTER_FLIP_X", "0") == "1"
POINTER_FLIP_Y = os.environ.get("MMDC_POINTER_FLIP_Y", "1") == "1"
MMDC_CONFIRM_REQUIRED = os.environ.get("MMDC_CONFIRM_REQUIRED", "0") == "1"
CONFIRM_TIMEOUT = float(os.environ.get("MMDC_CONFIRM_TIMEOUT", "2.0"))
CONFIRM_GESTURE = os.environ.get("MMDC_CONFIRM_GESTURE", "Open_Palm")
# Comma-separated list of actions to disable for safety, e.g. "open_explorer,save_document"
DISABLED_ACTIONS = set(filter(None, [s.strip() for s in os.environ.get("MMDC_DISABLED_ACTIONS", "").split(",")]))
