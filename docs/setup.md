# Local Setup & Running

Prerequisites
- Python 3.10 or 3.11
- git, curl, make (optional)
- On Linux, ensure OpenCV system deps are installed: `libgl1-mesa-glx` / `libgl1` or equivalent for your distro.

Quick start
1. Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install project dependencies (if `requirements.txt` exists):

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run tests:

```bash
python -m unittest discover -s tests -v
```

Running the prototype
- To run the app locally with a webcam: `python -m desktop_control_prototype.app`
- For headless testing (no webcam), set `MMDC_HEADLESS=1` in the environment. The code also checks for missing camera and exits gracefully.

Environment variables of interest
- `MMDC_CONFIRM_REQUIRED` — require confirmation for sensitive actions.
- `MMDC_DISABLED_ACTIONS` — comma-separated list of action names to disable during tests.
- `MMDC_ACTIVE_WINDOW_TITLE` — can be used to override profile detection for testing.

Packaging
- Build a wheel: `python -m build --wheel` (CI already performs this step).

Notes
- If your CI runner reports OpenCV errors, ensure system libraries are installed or mock out OpenCV in tests.
