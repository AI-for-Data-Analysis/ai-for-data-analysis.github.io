# Coding Agents for Analytics Work

This session uses Codex, a coding agent from OpenAI, to investigate a dataset and answer questions about it while keeping the work reproducible. This page covers the workspace and the requirements your analysis must meet before you write the first prompt.

## Workspace

The setup step prepares everything required. For this session:

- **JupyterLab** is the working environment.
- The **notebook** is the analysis artifact: the file you keep, rerun, and share.
- **Codex** is the coding agent, available in the assistant panel.
- The project contains a **`data/`** folder with the files to analyze.

Codex's work should run in the project environment created during setup and be written into the notebook.

### Opening JupyterLab and Accessing the Agent

When JupyterLab opens, it usually starts on the launcher screen. The launcher is the starting point for creating new notebooks, opening terminals or text files, and accessing extensions such as the coding agent chat.

```{figure} ../images/session-1/jupyter-lab-with-chat.png
:alt: JupyterLab launcher showing the Python notebook tile and the Chat tile
:width: 100%

The JupyterLab launcher includes both the notebook environment and the coding agent interface.
```

In the screenshot, **A** marks the Python notebook tile. Use this tile to create a new notebook for the analysis. The notebook is where the code, outputs, notes, and final analytical steps should live.

**B** marks the Chat tile. Use this tile to open the coding agent. The agent can help inspect files, write and revise code, run analysis, and update the notebook, but its work still needs to be reviewed and made traceable in the notebook.

After opening both tiles, arrange the chat and notebook side by side. This keeps the agent conversation visible while you review the code and output in the notebook.

```{figure} ../images/session-1/jupyter-lab-chat-notebook-side-by-side.png
:alt: JupyterLab with the coding agent chat open on the left and a Python notebook open on the right
:width: 100%

The coding agent chat and the analysis notebook can be open at the same time in the JupyterLab workspace.
```


## What a coding agent does

A coding agent is an AI assistant connected to a working project environment. Codex can read files, write Python, run that Python, edit files, and produce plots in the course of answering one request. It can change the project rather than only describing it.

This raises a requirement that does not apply to a chat assistant. When the output is code and analysis, that output must be possible to follow and verify because the answer depends on specific data, transformations, calculations, and assumptions. As we will see in the lessons, by default, Codex may run calculations in a temporary terminal, report a conclusion, and leave no corresponding code in the notebook. The result cannot then be checked or reproduced.

## Requirements for the analysis

Each analysis in this session must be:

- **Understandable** — the code and explanations can be read and followed.
- **Reviewable** — analytical steps are separated clearly enough to check individually.
- **Traceable** — every stated result corresponds to specific code and output.

## The process

The work proceeds as an iterative cycle rather than a single prompt:

```text
Run a prompt.
Review what Codex did.
Identify what was missing or incorrect.
Record a rule to correct it.
Run again, then continue into the analysis.
```

The remaining pages apply this cycle to the checkout dataset: an initial broad prompt, a set of project rules, a structured investigation of the data, and a trend analysis.
