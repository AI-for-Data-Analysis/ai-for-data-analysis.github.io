# Environments Version Control

## Why This Matters

Reproducibility is required for analytics review. Teams should execute environment setup themselves, with assistant guidance.

## Learning Objectives

- Create and use a project-local Python environment.
- Capture dependencies and run steps for repeatable analysis.
- Use version control checkpoints during assistant-driven development.

## Assistant-Guided, Learner-Executed Setup

Use the assistant to propose commands, then run and verify them yourself.

## Notebook-First Setup (Session 1 Baseline)

Mirror the cohort notebook setup:

`requirements.txt`:

```text
jupyterlab
jupyter-ai
pandas
matplotlib
plotly
```

Environment setup and launch:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

## Verification Checks

```bash
python -V
which python
```

Verification targets:

- Interpreter path points to `.venv`.
- JupyterLab launches from the project environment.
- Dependencies install without using global/base environments.
- A teammate can rerun the same steps from `README`.

## Minimal Project Contract

- `README.md`: setup and run instructions
- `requirements.txt` or `pyproject.toml`: dependency spec
- `notebooks/` or `src/`: analysis code
- `outputs/`: generated artifacts

## Version Control Milestones

Make small, meaningful commits:

1. Environment + baseline structure
2. Discovery artifact
3. First reproducible analysis
4. Validation/check updates

## Review Prompts for This Stage

```text
Check my repository for reproducibility gaps.
What would fail for a teammate cloning this project fresh?
```
