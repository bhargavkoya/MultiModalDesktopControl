# Release and packaging

Steps to build a wheel and source distribution locally:

```bash
source .venv/bin/activate
python -m pip install --upgrade build
python -m build
# artifacts will be in the `dist/` folder
```

To publish to PyPI (requires setup of credentials):

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

GitHub releases: create a release and upload the built artifacts from `dist/`.

Notes:
- The project uses a local console script `mmdc` defined in `pyproject.toml`.
- In many Linux containers OpenCV requires libGL (`libgl1-mesa-glx`).
