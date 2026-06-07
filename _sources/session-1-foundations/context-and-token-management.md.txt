---
orphan: true
---

# Context and Token Management

AI-assisted analysis is not only about writing better prompts. It is also about
managing what the agent is carrying from one step to the next.

For Session 1, use a simple mental model:

```{admonition} Mental model
:class: note

The current Codex conversation is temporary working context. The notebook,
`AGENTS.md`, README files, and saved outputs are the project record.
```

Temporary context is useful while you are solving one problem. It lets Codex
keep track of what it just inspected, what code it wrote, what errors appeared,
and what decisions you made. But it can also become cluttered. A long session
may contain old file previews, debugging output, abandoned approaches, large
notebook outputs, and decisions from a task that is already finished.

The goal is not to make every conversation short. The goal is to know when the
current conversation is still helping and when it is time to save the important
facts in the project and start fresh.

## What context includes

In a Codex session, context can include:

* system and project instructions
* the current conversation
* previous tool calls and their outputs
* file contents Codex has read
* notebook code and saved outputs
* error messages, plots, tables, and summaries

That context helps Codex answer follow-up questions. It also means a short
follow-up prompt may involve more work than the words you typed suggest. Codex
may need to use previous conversation, inspect files, read notebook cells, or
verify earlier work before answering.

The exact token accounting is system-dependent. For this lesson, the important
practice is simpler: do not rely on a long conversation as the only place where
important project knowledge lives.

## Why notebooks need boundaries

Notebooks are valuable because they keep code, output, and explanation together.
That is why we use them as the analysis artifact in this workshop.

But a notebook should not become a transcript of every scratch step. If Codex
repeatedly adds large previews, failed experiments, long stack traces, or
duplicated checks, the notebook becomes harder for people to review and harder
for future agent sessions to use.

A good notebook contains the code, output, and explanation needed to support the
analysis. It does not need every temporary preview or every abandoned attempt.

## When to start a fresh session

Start a new Codex session when the task changes enough that the old working
context is no longer useful.

Good boundaries include:

* after broad data profiling is complete
* before starting a new analysis question
* before switching from analysis to dashboard building
* before switching from analysis to stakeholder-facing explanation
* after a long debugging sequence
* after creating or revising `AGENTS.md`
* when the session has become mostly correction, cleanup, or backtracking

Starting fresh does not mean starting from nothing. It means moving verified
facts out of the conversation and into project files first.

## What to save before starting fresh

Before ending a session, ask what future Codex sessions and future humans need
to know.

Good project records include:

* a clean notebook section with code, output, and short explanation
* `data/README.md` with file meanings, row counts, schemas, and caveats
* `AGENTS.md` with standing project rules
* a short TODO list or decision note in a project Markdown file
* saved plots or tables that are referenced by the notebook
* notes about analysis choices, assumptions, caveats, and next steps

Poor project records include:

* a long terminal transcript that no one will reread
* a chat-only conclusion with no code behind it
* repeated data previews that do not add new information
* unverified conclusions copied from an agent response

A fresh session works best when Codex can start from compact, trustworthy
project files instead of reconstructing the project from a long chat.

## Run a quick usage report

This repository includes a small script that summarizes recent Codex sessions
from your local `~/.codex` folder:

```text
python tools/analyze_codex_usage.py --days 2
```

The script writes a `usage_reports/` folder with a Markdown summary, an HTML
report, and CSV files. For Session 1, use the report as a reflection tool. Look
for:

* sessions with many turns
* sessions that mixed several phases of work
* sessions where Codex repeatedly inspected files or notebook outputs
* places where a project note, README update, or fresh session might have helped

Do not treat the report as a perfect explanation of token billing. Use it to
notice patterns in how you worked.

## A quick check

Before you continue a long session, ask:

* Am I still working on the same task?
* Does Codex still need the previous debugging or exploration details?
* Have the important facts been saved in the notebook, `AGENTS.md`, a README, or
  another project file?
* Would a new session with a focused prompt be easier to review?

Keep going when the old context is still helping with the current task. Start
fresh when the useful facts have been saved and the remaining conversation is
mostly old exploration, debugging, or cleanup.

## Practical rules

Use these rules during the rest of the workshop:

* Keep the notebook as the analysis record, not as a transcript of
  every scratch step.
* Keep `data/README.md` as reusable project knowledge about the dataset.
* Start fresh when the phase of work changes.
* Ask Codex to inspect only the files or cells needed for the current question.
* Avoid printing large tables when a shape, column list, or compact summary is
  enough.
* Ask for a plan before implementation when the task is broad or ambiguous.
* Do not ask Codex to rediscover facts that are already in the notebook,
  `data/README.md`, `AGENTS.md`, or another project note.
* Move verified decisions into files before relying on them in later sessions.

```{admonition} Key points
:class: key

* Context is useful while it helps Codex solve the current task.
* Context becomes baggage when it contains old scratch work, large outputs, or
  details from a completed task.
* Fresh sessions are most useful when verified facts have already been saved in
  project files.
* The terminal-in-JupyterLab workflow keeps the notebook central while making
  context boundaries easier to control.
```
