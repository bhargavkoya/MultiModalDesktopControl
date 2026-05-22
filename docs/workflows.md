# Workflows & CI

CI pipeline (GitHub Actions)
- Workflow file: `.github/workflows/ci.yml` — runs on `pull_request` against `main` and (only) `push` to `main`.
- Matrix: Python `3.10` and `3.11` (quoted to avoid YAML float parsing issues).
- Steps: checkout, setup Python, install deps (from `requirements.txt` if present), run unit tests, build wheel, upload artifact.
- Concurrency: workflow uses `concurrency` to cancel duplicate in-flight runs for the same ref.

PR lifecycle
- Branches: feature branches are pushed and a PR opened against `main`.
- Checks: CI runs on PR; fix failures locally and push to update the PR.
- Merge: Review + merge when CI passes and reviews are satisfied.

Local CI troubleshooting
- If CI fails due to missing system libs (e.g., OpenCV `libGL`), install the required packages in the runner or adjust tests to run headless using `MMDC_HEADLESS`.

Suggested improvements
- Add caching for pip dependencies (`actions/cache`) and linting (`flake8`/`ruff`) steps to the workflow.
