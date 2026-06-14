# Session 1 Q&A

This page contains answers to questions left on sticky notes in Session 1.

## How do I analyze my own data with Codex?

Codex works from the folder where you start it. That folder is the project
workspace Codex can inspect, edit, and run commands in.

To analyze your own data, make a project folder first. Put your data files in
that folder, then start Codex from inside the project folder. A useful structure
is to keep the raw data in its own folder and keep notebooks, scripts, project
notes, and instructions one level above it:

```text
my-analysis-project/
├── .venv/
├── AGENTS.md
├── README.md
├── requirements.txt
├── analysis.ipynb
├── scripts/
└── data/
    ├── my_file.csv
    └── another_file.xlsx
```

This structure gives Codex a clear boundary: the project folder is the working
space, and `data/` is where the source files live. It also keeps analysis files
from getting mixed into the raw data folder.

Before analyzing the data, ask Codex to create a project-local Python virtual
environment. A virtual environment keeps the Python packages for this project
separate from the rest of your computer. For data analysis, the common
"scientific Python stack" includes packages such as `pandas`, `numpy`, `scipy`,
`matplotlib`, and Jupyter tools.

Ask Codex to set that up inside the project folder:

```text
Please create a project-local Python virtual environment in .venv, install the
basic scientific Python stack for data analysis, and save the package list in
requirements.txt. Do not install packages into the base Python or base conda
environment.
```

After Codex finishes, review what it did. You should see a `.venv/` folder and a
`requirements.txt` file. The virtual environment can be deleted and recreated,
but the requirements file should stay with the project so the setup can be
repeated later. If you use Git, commit `requirements.txt`, not the `.venv/`
folder.

Further reading: Python's documentation explains
[virtual environments](https://docs.python.org/3/library/venv.html), and the
SciPy project provides [installation guidance](https://scipy.org/install/) for
the scientific Python ecosystem.

````{admonition} How can I move my files to WSL?
:class: tip

If you are using WSL on Windows, the easiest way to move files into your Linux
project folder is often to open that folder in Windows File Explorer.

From the WSL terminal, move into your project folder and run:

```bash
explorer.exe .
```

The `.` means "this folder." File Explorer will open the current WSL directory,
and you can drag files into the project just like any other Windows folder.

After moving files, return to the WSL terminal and run `ls` to confirm they are
in the project folder.
````

Once the files are in place, open a terminal in the project folder and start
Codex there. Then ask Codex to inspect the data before analyzing it:

```text
Please inspect the files in data/. For each file, report the row count, column
names, data types, non-null counts, and the first few rows. Do not make plots
yet.
```
After Codex profiles the data, you can ask it to add project-specific guidance
to `AGENTS.md`. For example, if one file is sampled and another is complete,
write that down so future Codex sessions do not have to rediscover it.

## Does my data need to be formatted a certain way?

For this course, the important question is not whether the data is formatted for
an AI model. We are using AI-assisted programming for data analysis. That means
Codex is helping you write and run code, and the code still needs to read your
files through normal programming libraries.

Your data will be easiest to analyze when it is in a regular, tabular format
that tools like Python, pandas, R, Excel, Tableau, or databases can read
reliably. CSV, Excel, Parquet, JSON, and database tables can all work, depending
on the project. The key is consistency:

- one row should represent a consistent unit
- column names should be present and meaningful
- values in a column should have a consistent meaning
- dates, numbers, categories, and missing values should be represented
  consistently
- repeated tables, notes, merged cells, subtotals, and visual-only formatting
  should not be mixed into the analysis data

If your data is not already consistent, do not overwrite the original file. Keep
the raw data, create a cleaned or regularly formatted version, and save the code
that performs the conversion.

A useful project structure is:

```text
my-analysis-project/
├── AGENTS.md
├── README.md
├── analysis.ipynb
├── scripts/
│   └── prepare_data.py
└── data/
    ├── raw/
    │   └── original_file.xlsx
    └── processed/
        └── analysis_ready_file.csv
```

You can use Codex to help write the conversion script:

```text
Please inspect data/raw/original_file.xlsx and write a script that converts it
to a regular analysis-ready CSV in data/processed/. Preserve the raw file. Put
the conversion code in scripts/prepare_data.py and document any assumptions.
```

This gives you three things a reviewer can check: the original data, the
analysis-ready data, and the script that explains how one became the other.

## What are the pros and cons of using the command-line Codex versus the app version?

Both versions are Codex. The main difference is the working environment around
the agent.

The command-line version runs in your terminal. It is a good fit when you are
already working in a project folder, using shell commands, running Python
scripts, starting JupyterLab, checking files with `ls`, or using Git from the
command line. For this course, the CLI makes the project boundary very visible:
Codex starts in the directory you choose, reads files from that workspace, and
runs commands there.

The tradeoff is that the CLI expects you to be comfortable with terminal
workflow. You need to know where you are in the filesystem, how to move into the
right folder, and how to interpret command output. If the terminal is new to
you, this can make the first few steps feel less familiar.

The Codex app gives you a desktop interface for choosing projects, working with
threads, seeing diffs, using built-in Git tools, and running tasks in local,
worktree, or cloud mode. It also has an integrated terminal, so you can still run
project commands when needed. The app can be easier when you want a more visual
place to manage threads, review changes, or work on multiple projects.

The tradeoff is that the app can hide some of the filesystem mechanics that are
useful to learn. For data analysis, it is still important to understand which
project folder Codex is working in and where your data files are stored.

For this workshop, the command line is useful because it teaches the
mental model:

- make a project folder
- put the data inside the project
- start Codex from that project
- inspect the data before analyzing it
- save scripts, notebooks, and project notes alongside the data

After that model is clear, the app can be a convenient interface for the same
kind of work.

Further reading: OpenAI's Codex docs describe the [Codex CLI](https://developers.openai.com/codex/cli),
the [Codex app](https://developers.openai.com/codex/app), and
[Codex app features](https://developers.openai.com/codex/app/features).

## Should we worry about token usage for this course?

For this course, the main goal is to get comfortable using Codex for real data
analysis work. OIT is supporting your use during the course, so you should take
advantage of the opportunity to experiment as much as your available limits and
your own comfort allow.

That experimentation is part of the learning. Try asking Codex for a plan before
implementation. Try asking it to explain code it wrote. Try asking it to revise a
notebook section so the result is easier to review. Try starting a new thread
after saving project context. These repetitions are how the workflow becomes
less mysterious.

At the same time, comfort matters. Some people may want to be mindful of usage
limits, cost, or the energy use associated with generative AI systems. That is a
reasonable concern. You do not need to use Codex for every small task if that
does not feel right to you.

A practical balance is:

- use Codex enough to learn what it is good at and where you still need review
- ask focused questions instead of requesting huge unfocused outputs
- save useful findings in project files so you do not have to rediscover them
- stop when the tool is no longer helping your understanding

In short: be thoughtful, but do not be timid. This course is a supported chance
to try the tool, make mistakes, compare prompts, and build judgment about when
AI-assisted programming helps your analysis.

## Which slash commands and shortcuts should I learn first?

You do not need to memorize every Codex command. For this course, slash commands
are useful because they help you steer the session without changing the main
task.

Start with these:

- `/status`: check the current session, including model, permissions, context,
  and limits
- `/plan`: ask Codex to plan before changing files or writing code
- `/new`: start a fresh conversation in the same project when the task changes
- `/compact`: summarize a long conversation so the useful context is preserved
- `/mention`: attach a specific file or folder to the conversation
- `/model`: inspect or change the model when the task needs a different level of
  reasoning
- `/permissions`: review or change what Codex can do without asking first

The exact list can change, so the most important command is just `/`. Type `/`
in Codex to see what is available in your current environment.

The `@` pattern is also worth learning. You can use `@` path autocomplete, or
the `/mention` command, to point Codex at files that matter for the current
question. For example:

```text
Read @data/README.md and @analysis.ipynb. Then tell me whether the notebook
uses the right dataset for a monthly trend analysis.
```

This is not about using a special trick. It is about making context explicit. If
a file matters, do not make Codex guess which file to inspect.

Further reading: OpenAI's Codex docs describe
[CLI slash commands](https://developers.openai.com/codex/cli/slash-commands)
and [IDE slash commands](https://developers.openai.com/codex/ide/slash-commands).
