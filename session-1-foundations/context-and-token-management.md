# Managing Context in Coding Agent Conversations

Codex can appear to remember the whole project. It may refer to files it
inspected earlier, errors it saw, code it edited, or decisions you made several
prompts ago.

That behavior is useful, but it can also hide an important boundary. Codex does
not independently remember the project. Each response is generated from the
context the application gives the model: project instructions, conversation
history, file excerpts, tool results, command output, and the latest request.

For analytics work, the practical question is not only what to ask next. It is
also what should stay in the conversation and what should be written into the
project.

```{admonition} The central distinction
:class: note

Use the conversation for **working context**.

Use project files for **saved project context**.
```

Working context is the temporary material Codex needs to continue the current
task. It includes the current conversation, recent errors, command output,
notebook cells, file excerpts, and decisions made during the session.

Saved project context is different. It is information written into files so that
future humans and future Codex sessions can find it. The notebook, `AGENTS.md`,
`README.md`, `data/README.md`, scripts, tests, and short decision notes can all
serve this purpose.

The conversation can help discover facts. The project files should become the
place where verified facts live.

## Why this matters

A short prompt late in a session can depend on a long history of work:

```text
Make the chart clearer.
```

That prompt may depend on earlier decisions about which CSV contains full
checkout totals, which files are samples, whether 2026 is partial, and what the
notebook section is trying to show. If those facts live only in the conversation,
Codex may need to carry them forward, summarize them, or rediscover them later.

That can waste time, tokens, and attention. More importantly, it can make the
analysis harder to review. A result is not very traceable if the reason for it is
buried in an old chat turn instead of recorded near the notebook code or in a
data note.

In the checkout project, suppose Codex learns that
`combined_checkout_totals_by_month_usageclass.csv` is monthly aggregate data,
that the two title-level files are balanced samples, that the aggregate file
should be used for full checkout volume trends, and that 2026 is partial.
Those facts affect which analysis is valid. They should not live only in the
chat. They belong in the notebook, `data/README.md`, or another project note.

## What should be saved

Not every detail deserves a permanent note. A temporary stack trace usually does
not need to be saved after the bug is fixed. A failed plotting attempt usually
does not belong in the final notebook unless it explains a lasting decision.

Save context when it will help a future session avoid rediscovering something
important or avoid repeating a mistake. Dataset meanings, row-level definitions,
sample-versus-aggregate distinctions, partial-year caveats, reusable commands,
and standing workflow rules are usually worth saving. Put them where someone
would naturally look: dataset facts in `data/README.md`, analysis decisions near
the relevant notebook code, and standing instructions in `AGENTS.md`.

Good saved context is short, verified, and placed close to the work it explains.
Poor saved context is a long terminal transcript, a chat-only conclusion,
repeated previews, or unverified claims copied from an agent response.

## Manage context while you work

The goal is not to keep conversations short at all costs. A long session can be
useful when it stays focused on one task. The problem is old context that no
longer helps with the current task.

Use the same conversation when the previous context is still helping: for
example, while working through one bug, one analysis question, one notebook
section, one visualization, or one focused data investigation.

Start fresh when the phase of work changes and the important facts have been
saved. This is often useful after broad data profiling, before starting a new
analysis question, after a long debugging sequence, or when Codex keeps referring
to an old assumption.

If the conversation is long but still relevant, `/compact` can help by replacing
older history with a summary. Compaction is useful, but it is lossy. A summary
may lose exact file names, column names, code details, or the reason a decision
was made. Compaction is not a substitute for saving important context in project
files.

```{admonition} Practical rule
:class: tip

Before starting fresh or compacting, ask: what would the next analyst need to
know?
```

## Choose model and reasoning level

Context management is not only about what you put in the prompt. It is also
about choosing the right model behavior for the work.

A stronger reasoning model or a higher reasoning setting can be useful when the
task has many dependencies: debugging a notebook failure, comparing possible
analysis plans, deciding which dataset supports a question, or reviewing whether
a conclusion follows from the code. Those tasks require the model to hold several
constraints in mind and test alternatives before it acts.

That extra reasoning is not free. Reasoning uses tokens, takes time, and still
depends on the quality of the context you provide. If the model has the wrong
file, stale assumptions, or a vague goal, more reasoning can produce a more
elaborate wrong answer.

Use a faster or lower-reasoning setting when the task is narrow and mechanical:
fixing a typo, reformatting a small table, renaming a chart title, or applying a
specific edit you can describe clearly.

Use a stronger or higher-reasoning setting when the task requires judgment:
choosing an analysis approach, tracing a result back to source files, debugging
an error with several possible causes, or reviewing whether a notebook section is
understandable, reviewable, and traceable.

```{admonition} Practical rule
:class: tip

First improve the context. Then increase reasoning if the task still requires
more planning, comparison, or debugging.
```

In Codex, use `/help` to see the model controls available in your installed
version. If `/model` is available, use it to inspect or change the current model
for the session. Model names and available reasoning settings can change, so do
not memorize a single model name as the lesson. The transferable skill is knowing
what kind of work you are asking the model to do.

## Ask for focused evidence

Context also grows when Codex prints more than the task requires. Ask for the
smallest useful evidence.

For example, instead of asking Codex to print a whole file, ask for the column
names, row count, data types, and first three rows. Instead of asking for every
group count, ask for the top ten values and the number of distinct values.
Instead of asking for a broad project scan, ask Codex to inspect only the
notebook and data files needed for the current trend question.

Focused output keeps the working context smaller and makes human review easier.

## Activity: decide where context belongs

At the end of an analysis step, choose three facts or decisions Codex learned
during the session. For each one, decide whether it should stay only in the
conversation, be added to the notebook, be added to `data/README.md`, or become a
rule in `AGENTS.md`.

Then ask Codex to update only the appropriate file:

```text
Please update the project notes so a fresh Codex session can continue from the
verified context we just established.

Put dataset facts in data/README.md, analysis decisions near the relevant
notebook section, and standing workflow rules in AGENTS.md. Do not preserve
temporary errors unless they explain a lasting decision.
```

Review the edits before keeping them. Make sure Codex saved verified facts, not
guesses.

## Useful Codex commands

In the Codex CLI, type `/` to see available slash commands. The exact list may
change, so use `/help` as the source of truth.

For context management, `/status` is useful when you want to check the current
session state. `/compact` is useful when the conversation is long but still
relevant. `/new` is useful when old context is no longer helping. `/resume` and
`/fork` are useful when you intentionally want to return to or branch from a
saved conversation.

These commands manage the conversation. They do not replace good project
records.

## Optional: run a usage report

You can download a small analysis script that summarizes recent Codex sessions
from your local `~/.codex` folder. From the project folder, create a `scripts/`
directory and retrieve the script with `curl`:

```bash
mkdir -p scripts
curl -L \
  -o scripts/analyze_codex.py \
  https://gist.githubusercontent.com/janash/d057c92b75f5a3f7990eedf3ecb0927a/raw/01958db1bcc0360b6f22d0d7ff3af42ecab0aee0/analyze_codex.py
```

Then run it:

```bash
python scripts/analyze_codex.py --days 2
```

The script writes a `usage_reports/` folder with a Markdown summary, an HTML
report, and CSV files. Use the report as a reflection tool. Look for sessions
that mixed several phases of work, repeatedly inspected the same files, or
produced large outputs where a project note or fresh session might have helped.

Do not treat the report as a perfect explanation of billing. Use it to notice
patterns in how you worked.

```{admonition} Key points
:class: key

- Codex conversations are useful working context, not saved project context.
- Verified facts, decisions, caveats, and reusable commands should be written
  into project files.
- Start fresh when old context stops helping, but only after the important facts
  have been saved.
- Match the model and reasoning level to the task: use more reasoning for
  planning, debugging, and review; use less for narrow mechanical edits.
- Ask for focused evidence instead of large outputs.
```
