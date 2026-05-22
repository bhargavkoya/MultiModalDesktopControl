# Architecture Overview

This project implements a gesture-driven desktop control prototype with a small, testable architecture focused on safety and modularity.

Core components
- `tracker`: MediaPipe/OpenCV-based hand tracking which yields normalized landmarks.
- `intents`: Gesture → Intent mapping and profile-aware routing (Explorer, Word, default).
- `pointer_calibration`: Maps camera-normalized points to screen-space with configurable spans and flips.
- `pointer_interactions`: Handles pinch/click vs drag semantics and gesture state.
- `desktop_controller`: Safe wrappers around `pyautogui` for mouse/keyboard actions.
- `confirm_manager`: Gating for sensitive actions (confirmation required, timeout, confirm gesture).
- `command_adapter`: Text/LLM command parsing into `Intent` objects (testable stub).
- `overlay`: OpenCV overlay for visual feedback and confirmation prompts.

State machine & modes
- Mode-based control determines which gestures map to which intents: `IDLE`, `POINTER`, `COMMAND`, `LAUNCHER`, `EXPLORER_NAV`, `APP_CONTROL`, `PAUSED`.
- Gesture flow: Gesture → classified `Intent` → profile-adapted `Action` → `desktop_controller` side-effect (confirmed when required).

Configuration
- Runtime tuning in `desktop_control_prototype/config.py` (pointer smoothing, pinch threshold, drag hold seconds, confirm settings).

Testing and safety
- Unit tests live in `tests/` covering intents, pointer calibration, confirm manager, and interactions.
- CI runs tests and builds a wheel; dangerous actions guarded by `MMDC_CONFIRM_REQUIRED` and `MMDC_DISABLED_ACTIONS`.

Where to start
- Read the runner: `desktop_control_prototype/app.py` to understand the main loop and how components connect.
