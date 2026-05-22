Title: Prototype: Add local testing workflows and core prototype features

Summary

This PR adds local testing documentation and implements multiple prototype features to make the webcam-driven desktop-control prototype more testable and safer for local use.

Key changes (high level)

- Pointer calibration: configurable bounds and flips (`pointer_calibration.py`, `config.py`).
- Pointer interactions: click vs drag timing, drag support (`pointer_interactions.py`, controller mouse_down/mouse_up/drag_to`).
- Profiles & intents: Explorer and Word profiles, robust active-window detection (`app_profiles.py`, `intents.py`).
- Runtime wiring: pointer smoothing, profile-based intents, command adapter, confirmation gating, and overlay updates (`app.py`, `overlay.py`).
- Command adapter: local text -> `Intent` mapping for testing and LLM integration placeholder (`command_adapter.py`).
- Safety: confirmation manager and gesture-based confirmation fallback, disabled-action opt-out (`confirm_manager.py`, updated config). 
- Tests: Extensive unit tests added and updated under `tests/` (pointer, interactions, profiles, commands, confirm manager).
- Packaging & CI: `pyproject.toml`, `RELEASE.md`, and GitHub Actions CI (`.github/workflows/ci.yml`) to run tests and build wheel on push/PR.
- Docs: `LOCAL_WORKFLOWS.md` (local testing workflows), README updates.

Files of special interest

- `desktop_control_prototype/app.py` — runtime loop and wiring
- `desktop_control_prototype/pointer_calibration.py` — mapping camera-normalized coords
- `desktop_control_prototype/pointer_interactions.py` — hold/drag timing state
- `desktop_control_prototype/command_adapter.py` — offline command parsing
- `desktop_control_prototype/confirm_manager.py` — confirmation gating
- `desktop_control_prototype/app_profiles.py` — profile detection and mapping
- `tests/` — new and updated unit tests
- `.github/workflows/ci.yml` — CI to run tests and build wheel

How to test locally

1) Run unit tests (recommended):

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
```

2) Quick command-mode smoke test:

```bash
# Execute a one-off command via env var
MMDC_COMMAND="Open Explorer" python -m desktop_control_prototype.app
# Note: MMDC_COMMAND executes immediately and is cleared after one run.
# Confirmation-required behavior applies to gesture-triggered sensitive actions.
```

3) Pointer calibration and manual testing (use a laptop or host webcam; containers may not have a camera):

```bash
# Tune pointer reach
MMDC_POINTER_X_MIN=0.08 MMDC_POINTER_X_MAX=0.92 MMDC_POINTER_Y_MIN=0.08 MMDC_POINTER_Y_MAX=0.92 \
  python -m desktop_control_prototype.app
```

4) Test profile routing

```bash
# Simulate active window title for Explorer or Word
MMDC_ACTIVE_WINDOW_TITLE="File Explorer" python -m desktop_control_prototype.app
MMDC_ACTIVE_WINDOW_TITLE="Microsoft Word - Document1" python -m desktop_control_prototype.app
```

5) Drag vs click

- Enter pointer mode (gesture or via command): `MMDC_COMMAND="pointer mode"`.
- Use a pinch (or simulated landmarks) to verify short pinch = click, long pinch = drag.

Notes & safety

- Use `MMDC_CONFIRM_REQUIRED=1` and `MMDC_CONFIRM_GESTURE=Open_Palm` to require gesture-based confirmation for sensitive actions.
- Disable actions via `MMDC_DISABLED_ACTIONS="open_explorer,save_document"` for extra safety.

CI & packaging

- GitHub Actions workflow runs tests and builds a wheel for Python 3.10/3.11; artifact uploaded.
- Build locally with `python -m build` after installing `build`.
