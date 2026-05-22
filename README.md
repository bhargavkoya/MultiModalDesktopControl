# MultiModalDesktopControl

Prototype for webcam-driven desktop control.

## Run

```bash
source .venv/bin/activate
python -m desktop_control_prototype.app
```

## Profile overrides

- Set `MMDC_ACTIVE_WINDOW_TITLE` to simulate the focused app.
- Example: `File Explorer` enables Explorer actions.
- Example: `Microsoft Word - Document1` enables Word shortcuts.

### Word profile

- `Open_Palm` in IDLE enters App Control mode for Word.
- In App Control mode: `Pinch` = Save, `Open_Palm` = Find, `Pointing` = Select All, `Closed_Fist` = Bold.

## Pointer calibration

- `MMDC_POINTER_X_MIN` / `MMDC_POINTER_X_MAX` tune horizontal reach.
- `MMDC_POINTER_Y_MIN` / `MMDC_POINTER_Y_MAX` tune vertical reach.
- `MMDC_POINTER_FLIP_X=1` flips the horizontal axis.
- `MMDC_POINTER_FLIP_Y=1` flips the vertical axis.

## Tests

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
```