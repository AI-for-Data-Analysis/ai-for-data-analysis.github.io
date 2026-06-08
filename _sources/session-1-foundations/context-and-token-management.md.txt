---
orphan: true
---

# Managing Context in Coding Agent Conversations

When you work with Codex, it can feel as if the agent remembers the whole
project. It may refer to files it inspected earlier, errors it saw, code it
edited, or decisions you made ten prompts ago.

That feeling is useful, but it can also be misleading. The language model does
not remember the project on its own. Codex is an application around the model.
For each response, the application gives the model a working context: selected
instructions, conversation history, tool results, file excerpts, and the latest
request.

For data analysis, the practical question is not only:

```text
What should I ask Codex next?
```

It is also:

```text
What context should Codex keep using, and what should be saved somewhere more durable?
```

```{admonition} The central distinction
:class: note

Use the conversation for **working context**.

Use project files for **durable context**.
```

## Why this matters for analysts

Data analysis work creates a lot of temporary information:

* file previews
* column lists
* missing-value checks
* failed plotting attempts
* stack traces
* partial interpretations
* caveats about sampling or aggregation
* decisions about which dataset answers which question

Some of that information is useful only for the next few minutes. Some of it is
important project knowledge.

For example, suppose Codex inspects the checkout data and learns this:

```text
combined_checkout_totals_by_month_usageclass.csv is monthly aggregate data.
The two title-level checkout files are balanced samples.
The aggregate file should be used for full checkout volume trends.
The 2026 data is partial.
```

Those facts should not live only in the chat. They affect which analysis is
valid, which plots are misleading, and how future work should proceed. They
belong in the notebook, a `data/README.md`, or another project note.

The conversation can help discover the facts. The project should become the
place where verified facts live.

## Working context and durable context

**Working context** is what helps Codex continue the current task. It may
include:

* the current conversation
* project instructions
* files Codex has inspected
* commands Codex has run
* tool outputs
* error messages
* notebook cells and outputs
* decisions made during the current task

Working context is valuable while you are solving one problem. If Codex just ran
a cell, saw an error, and is about to fix it, that error is useful context. If
Codex just compared two plotting approaches and you chose one, that decision is
useful context.

**Durable context** is information saved where future humans and future agent
sessions can find it. It may include:

* the notebook
* `AGENTS.md`
* `README.md`
* `data/README.md`
* saved plots and tables
* tests
* scripts
* commit history
* short decision notes

Durable context is what lets a fresh session start from trusted project
knowledge instead of reconstructing the project from an old chat.

```{list-table}
:header-rows: 1

* - If Codex learns...
  - Save it in...
* - what each data file contains
  - `data/README.md` or a notebook data inventory section
* - what one row represents
  - the notebook and data notes
* - which file should answer a question
  - the notebook near the analysis code
* - raw data should not be modified
  - `AGENTS.md`
* - the command to run the analysis
  - `README.md`
* - a caveat such as "2026 is partial"
  - the notebook near the chart or conclusion
* - a temporary stack trace from one failed attempt
  - usually nowhere, unless it explains a lasting decision
```

## A coding agent is a system, not just a chat box

It helps to separate the parts of the system.

The **model** generates the next response from the context it receives. It does
not independently remember earlier conversations.

The **Codex application** manages the session. It can keep conversation history,
send tool definitions, pass along tool results, and decide what setup context is
needed for the next model call.

The **tools** act on the project. They can read files, run commands, edit code,
or inspect outputs, depending on what is available and permitted.

The **project files** are the durable record. They are the source future humans
and future agent sessions can inspect.

This boundary matters. If Codex gives a good explanation in chat but does not
write the reasoning into the notebook, the analysis is not yet traceable. If it
discovers a dataset caveat but the caveat stays only in the conversation, the
next session may have to rediscover it.

## Context affects token use

Tokens are the pieces of text the model processes. Your latest prompt is only
one part of token use.

In a coding-agent session, token use may also reflect:

* earlier conversation
* project instructions
* file excerpts
* command output
* notebook output
* error messages
* summaries of earlier work
* the model's own response

That is why a short prompt late in a long session may involve more context than
the visible words suggest.

The exact accounting can be more complicated than "the whole chat is resent
every time." Systems may use stored conversation state, prompt caching, or
compaction. Those mechanisms can change what is physically sent or how repeated
context is billed.

For this lesson, the practical rule is simpler:

```{admonition} Practical rule
:class: tip

Do not manage cost by looking only at the length of your latest message.

Manage cost by managing the relevance of the working context.
```

Relevant context helps Codex do the task. Irrelevant context creates clutter.

## How context gets cluttered

Context clutter is common in exploratory analytics work.

It can happen when:

* one conversation mixes data inventory, cleaning, plotting, debugging, and
  stakeholder writing
* Codex repeatedly inspects the same files because important findings were not
  saved
* large tables are printed when a compact summary would do
* broad searches return many irrelevant files
* long stack traces remain central after the bug is fixed
* abandoned analysis paths stay mixed with the current direction
* notebook outputs become large enough that they distract from the analysis

The issue is not that long sessions are always bad. A long session can be useful
when it is focused on one task. The issue is whether the old context still helps
with the current task.

## Keep going, compact, or start fresh

Keep using the same conversation when the previous context is still helping.
That is usually true when you are working on:

* one bug
* one analysis question
* one notebook section
* one visualization
* one focused data investigation

Start fresh when the old context is no longer helping. That is often true:

* after broad data profiling is complete
* before starting a new analysis question
* before switching from exploration to dashboard building
* before switching from analysis to stakeholder-facing explanation
* after a long debugging sequence
* after important findings have been saved into project files
* when Codex keeps referring to an old assumption
* when the session has become mostly correction, cleanup, or backtracking

If the conversation is long but still relevant, compaction can help by replacing
older history with a summary. Compaction is useful, but it is lossy. A summary
may lose exact file names, column names, code details, or the reason a decision
was made.

That is why compaction is not a substitute for project records.

## What to save before starting fresh

Before ending a session, ask:

```text
What would the next analyst need to know?
What would a fresh Codex session need to know?
What would be expensive or risky to rediscover?
```

Good things to save include:

* dataset names and meanings
* row counts and column names
* what one row represents
* whether data is sampled, aggregated, or complete
* which file supports which question
* assumptions and caveats
* commands that run the analysis
* decisions about plots or methods
* project rules Codex should follow next time
* next steps

Poor project records include:

* a long terminal transcript no one will reread
* a chat-only conclusion with no code behind it
* repeated data previews that do not add new information
* unverified claims copied from an agent response
* notebook sections full of failed scratch attempts

## Ask for targeted output

One of the easiest ways to manage context is to ask for the smallest useful
evidence.

Instead of asking Codex to print a whole file, ask for:

```text
Show the column names, row count, data types, and the first 3 rows.
```

Instead of asking for every group count, ask for:

```text
Show the top 10 values for this column and report how many distinct values it has.
```

Instead of asking for a broad project scan, ask for:

```text
Inspect the notebook and the files in data/ that are needed to answer this trend question.
```

Targeted output is not just tidier. It makes the agent's working context more
focused and the human review easier.

## Activity: move context into the project

At the end of an analysis step, choose three facts Codex learned during the
session.

For each one, decide where it belongs:

```{list-table}
:header-rows: 1

* - Fact or decision
  - Keep only in conversation?
  - Save in notebook?
  - Save in `data/README.md`?
  - Save in `AGENTS.md`?
* - What does one row represent?
  - No
  - Yes
  - Yes
  - No
* - Raw data files should not be modified
  - No
  - Maybe
  - No
  - Yes
* - One failed plotting attempt produced a temporary error
  - Usually yes
  - Only if it affects the final method
  - No
  - No
```

Then write or update the appropriate project note.

The goal is not to document everything. The goal is to save the facts that make
future work more accurate, reproducible, and efficient.

## Useful Codex commands

In the Codex CLI, type `/` to see available slash commands. The exact list may
change, but these are useful for context management:

```{list-table}
:header-rows: 1

* - Command
  - Use it when...
* - `/status`
  - you want to check the current session state, including context-window information
* - `/compact`
  - the conversation is long but still relevant, and you want Codex to summarize older context
* - `/new`
  - the old context is no longer useful and you want a fresh conversation
* - `/resume`
  - you intentionally want to return to a saved conversation
* - `/fork`
  - you want to branch from the current conversation and try a different direction
```

These commands manage the conversation. They do not replace good project
records.

## Optional: run a usage report

This repository includes a small script that summarizes recent Codex sessions
from your local `~/.codex` folder:

```text
python tools/analyze_codex_usage.py --days 2
```

The script writes a `usage_reports/` folder with a Markdown summary, an HTML
report, and CSV files.

Use the report as a reflection tool. Look for:

* sessions with many turns
* sessions that mixed several phases of work
* sessions where Codex repeatedly inspected files or notebook outputs
* places where a project note, README update, or fresh session might have helped

Do not treat the report as a perfect explanation of billing. Use it to notice
patterns in how you worked.

## Practical rules for the workshop

Use these rules during the rest of the workshop:

* Keep the notebook as the analysis record, not a transcript of every scratch
  step.
* Keep `data/README.md` as reusable project knowledge about the dataset.
* Keep `AGENTS.md` for standing rules Codex should follow.
* Ask Codex to inspect only the files or cells needed for the current question.
* Avoid printing large tables when a shape, column list, or compact summary is
  enough.
* Ask for a plan before implementation when the task is broad or ambiguous.
* Start fresh when the phase of work changes and the important facts have been
  saved.
* Do not ask Codex to rediscover facts that are already in the notebook,
  `data/README.md`, `AGENTS.md`, or another project note.

```{admonition} Key points
:class: key

* Codex conversations are useful working context, not durable project memory.
* A short prompt can still depend on a large amount of prior context.
* Large outputs, repeated failed attempts, and old assumptions can make context
  less useful.
* Verified facts, decisions, caveats, and reusable commands should be written
  into project files.
* Start fresh when the old conversation stops helping, but start from the files
  that now contain the important context.
```
