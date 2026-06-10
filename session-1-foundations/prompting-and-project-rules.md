# Prompting and Project Rules

A **prompt** is an instruction or message given to an AI system. It can ask a question, request an action, provide context, point the AI toward specific files, or tell it what kind of output to produce. In this lesson, prompts are the messages you type to Codex in the JupyterLab terminal.

Working with a coding agent is often iterative, especially at the beginning of a project. You ask for something, observe what the agent does, and then refine either the next prompt or the standing project instructions. The first prompt does not need to be perfect, but each response gives you evidence about what the agent needs to be told more explicitly.

As the project develops, the interaction may become less repetitive. Once expectations are recorded in `AGENTS.md` and the notebook contains more context, later prompts can often be shorter because Codex has more project guidance to work from.

The wording of a prompt determines what Codex does for the immediate task. A project rules file determines how Codex should work across the project. In this lesson, we first observe what Codex does with broad and notebook-focused prompts, then turn those observations into starter rules in `AGENTS.md`.

## Sessions are separate contexts

Each new Codex session starts a new conversation context. Codex does not automatically know what you discussed in a different session unless that information is available in the project files, the open notebook, or the current conversation.

This is useful when you are trying different things. For example, you might use one session to investigate the data, another session to revise project rules, and another session to work on a specific visualization. Separate sessions help keep those tasks from blurring together.

The tradeoff is that context does not magically carry over. If a decision matters across sessions, record it somewhere durable: in the notebook, in `AGENTS.md`, in a README, or in another project file. Treat the session as the working conversation and the project files as the shared memory.

In the first part of this lesson, we intentionally try several prompts in
different sessions. That makes the context boundary visible: each new session may need
to inspect the repository and data again before it can answer well. That repeated
orientation is not a mistake, but it is work we can reduce once the project
starts to take shape. As the project develops, we can write important context
into project files and record standing expectations in `AGENTS.md`.

The goal is not to prevent Codex from working quickly. The goal is to make sure its speed produces analysis that can be inspected, revised, and rerun. The workflow is:

- Try a prompt.
- Observe what Codex does.
- Identify what should be more reviewable.
- Record standing expectations in `AGENTS.md`.
- Try again with those expectations in place.

## Try one broad prompt before rules

Start with a broad request before adding project rules. This makes Codex's default behavior visible.

```{admonition} Codex in the JupyterLab terminal
:class: warning

In the terminal workflow, type the prompt directly into Codex. Do not include `@Codex`; that mention was only needed in the earlier Jupyter chat workflow.
```

In the Codex terminal, enter:

```text
I need to do exploratory data analysis on the data in my seattle-public-library folder. Can you investigate and tell me about it?
```

Watch what Codex does before evaluating the answer. Note whether it writes reusable notebook code, works in the terminal, summarizes in the response, creates files, or makes assumptions about the data.

## What Codex did

```{note}
Because coding agents use LLMs and can choose different valid paths through a task, your run may not match this sequence exactly. You may see different commands, a different order of operations, or slightly different wording in the final response. The important pattern is whether Codex leaves behind work that is easy to inspect and rerun.
```

In testing, Codex inspected the project structure and the files in `data/`. Your run might do this in a different order, but it should find three CSVs:

```text
combined_checkout_totals_by_month_usageclass.csv
digital_checkout_title_sample_balanced_250k.csv
physical_checkout_title_sample_balanced_250k.csv
```

Codex might run file and environment checks, including commands such as:

```text
pwd
List data
Read digital_checkout_title_sample_balanced_250k.csv
Read physical_checkout_title_sample_balanced_250k.csv
Read combined_checkout_totals_by_month_usageclass.csv
wc -l data/*.csv
```

It then might write and execute Python code in the terminal to compute:

```text
dataset shapes
columns and dtypes
missingness
date ranges
usageclass counts
checkouttype counts
materialtype counts
checkout summaries
top creators
top publishers
top titles
top subject tokens
rows by year
yearly totals and shares
```

## What Codex reported

Codex might produce a polished EDA summary. In testing, it identified:

```text
combined_checkout_totals_by_month_usageclass.csv: 501 rows, monthly aggregate data from April 2005 through April 2026.
digital_checkout_title_sample_balanced_250k.csv: 250,000 sampled digital title-month rows.
physical_checkout_title_sample_balanced_250k.csv: 250,000 sampled physical title-month rows.
```

It might also surface findings such as:

```text
Physical checkouts dominated from 2005 through 2019.
Digital grew gradually and became the majority in 2020.
The two title-level files are balanced samples, not full raw extracts.
The aggregate file should be used for full checkout volume trends.
```

## What this demonstrates

Codex may do a lot from a vague prompt. That is useful for quick orientation, but the work may not be very traceable. Much of the analysis may happen in temporary terminal code, and the final output may be a response summary rather than a reusable notebook artifact.

The broad prompt is useful here as a teaching demonstration, but it is not the most efficient way to work. It may spend tokens on a wide scan, a long summary, or analysis steps that do not become part of the notebook. The request also did not specify where the work should be recorded, ask Codex to keep the code simple, explain the data structure before interpreting trends, or leave behind a notebook section that another person could review.

## Try a notebook prompt

Next, ask Codex to put the investigation into the notebook:

```text
Can you help me investigate the data in my seattle-public-library folder? I would like to know what the dataset or datasets are and the relationships between the items.

I have a notebook open. Please add a brief Data Inventory section that previews each file, summarizes the rows and columns, and explains what one row seems to represent.
```

This prompt demonstrates a capability that response summaries do not show: Codex can edit the notebook itself, adding code cells and explanatory text instead of only answering in the terminal.

For this activity, the desired notebook shape is intentionally basic: a short
markdown setup, a code cell that previews the data files, a compact summary
table, and a few cautions about interpretation. The prompt does not spell all of
that out, so the class can observe whether Codex makes reasonable choices or
adds too much.

It also gives us something important to inspect: the kind of notebook code Codex might write before we give it project rules. Even with this basic request, the code may run correctly but still be difficult to review. For example, Codex may combine several analytical steps into one compact pandas expression, use helper columns without explaining them, or write more explanation than the notebook needs.

You may also see Codex do substantial profiling in the terminal before it edits
the notebook. That can be useful scratch work, but it is a problem if the
important reasoning only appears in terminal output or a response summary. For this course, the
durable artifacts should be the notebook and project files. If Codex keeps
rediscovering the same dataset facts in scratch commands, that is a signal to
write those facts down where future sessions can find them.

However, this prompt still leaves important interpretation questions implicit. It asks about "datasets" and "relationships," but it does not explicitly require Codex to answer:

- What does one row represent?
- What is being counted?
- Is each file sampled, aggregated, or complete?
- What would be misleading to infer from each file?

The narrower prompts improve the immediate task, but they do not solve the whole workflow problem. We still need project rules that tell Codex what reviewable notebook code should look like and require it to clarify the data structure before analysis.

These first prompts motivate the need for rules. We do not need to wait until the notebook is messy to define expectations. After observing Codex with broad and narrower prompts, we can already see that it needs guidance about simple code, traceable work, and understanding the data structure before analysis.

```{admonition} Exercise: Draft rules from observation
:class: exercise

In your group, review what Codex did across the first prompts. Draft three rules that would make its analytics work easier to inspect, revise, or rerun.

For each rule, write down the observation that motivated it. For example:

- Observation: Codex answered in the terminal but did not leave notebook code.
- Rule: Put investigation code and short explanations in the open notebook.

Keep the rules short. You will compare them with the starter `AGENTS.md` rules in the next section.
```

## Show how AGENTS.md works

`AGENTS.md` is a project instruction file: a plain Markdown file that lives in
the project folder and gives coding agents standing instructions for how to work
in that project. It is not a Python file, a notebook file, or a data file. It is
also not unique to this dataset; it is an [AGENTS.md convention](https://agents.md/)
used by coding-agent tools to find project-specific guidance.

In this workshop, we use `AGENTS.md` to tell Codex how to handle analytics work
in this repository. Once Codex has been asked to write in a notebook during a
session, it may continue doing that within the same conversation. But if
notebook-based, traceable analysis is an expectation for the whole project, we do
not want to retype that instruction at the start of every new session. `AGENTS.md`
gives us a place to record those standing expectations so they can be loaded
automatically.

Create a file called `AGENTS.md` and use a temporary rule to make the instruction
mechanism visible. Add this section to `AGENTS.md`:

```markdown
## Response Style Test

Answer in haiku.
```

In codex, open a new thread using the `/new` command.

Ask Codex a simple question and observe whether the response changes. If the response is formatted as a haiku, the project rules are reaching the agent.

Then remove the haiku rule. The haiku test is not part of the analytics workflow; it simply shows that Codex is reading project instructions.

```{admonition} Start a new session after changing AGENTS.md
:class: warning

After changing `AGENTS.md`, start a new Codex session before testing the new rule. Existing sessions may already have loaded the previous instructions. Starting a new session is the clearest way to make sure Codex reads the updated file. This is another example of the same context principle: a new session starts fresh, then loads the current project instructions.
```

## Add first-round AGENTS.md rules

Now replace the temporary rule with a small set of non-negotiable rules for analytics work. Later, groups will add their own rules based on what they observe.

After updating `AGENTS.md`, start a new Codex session again so the starter analytics rules are loaded for the next prompt.

Update `AGENTS.md` with the starter rules below, and fill in the Python experience level for your audience.

```markdown
# AGENTS.md

## Purpose

This project is for an AI-assisted analytics workflow.

We are using Codex to help investigate data, write Python code, create notebook explanations, and build reproducible analysis artifacts.

## Audience and Experience Level

Notebook code should be written for a student with one semester of Python
experience. Use explicit, step-by-step pandas code with descriptive intermediate
variables. Avoid compact idioms, dense method chaining, and unexplained
reshaping or aggregation shortcuts.

## Non-Negotiable Rules

1. Treat the notebook as the durable analysis record, not as a full transcript of scratch work. For accepted analysis, write the code, outputs, checks, and short explanations needed to understand and rerun the result.

2. Inspect actual files and data before making claims, but do not repeatedly re-investigate the same data when the notebook already contains sufficient evidence.

3. If a new question depends on information not yet established in the notebook, add only the minimal new inspection needed to answer it.

4. Do not run separate terminal or scratch Python analysis to preview, verify, or compute results that belong in the accepted notebook analysis. Terminal commands may be used for non-analytical maintenance, such as file existence checks, notebook structure checks, and environment checks.

5. Do not modify raw data files.

6. Do not duplicate accepted analysis work. If a table, chart, statistic, join, data profile, or interpretation will support a notebook claim, compute it in the notebook only.

7. Make transformations explicit, readable, and rerunnable.

8. Do not invent column names, file names, metadata, or dataset meanings.

9. Keep the notebook clean. Include durable inspection, analysis, transformations, checks, outputs, and short explanations that support the work. Do not include irrelevant experiments, repeated previews, or exploratory dead ends unless they explain an important decision.

10. Before creating plots or interpreting trends, identify what one row represents, what value is being counted or aggregated, and whether the data is sampled, aggregated, or complete.
```

`AGENTS.md` applies to the whole project and is loaded automatically when a new agent session starts. A prompt shapes the immediate task; `AGENTS.md` records the standing instructions you want Codex to carry into each new task in this project.

```{admonition} Exercise: Add and test your own rule
:class: exercise

Add one small rule to `AGENTS.md` that would make Codex's notebook work easier for you to review. Start a new Codex session, then ask Codex a short question or revision request that should reveal whether the rule is being followed.

After testing, decide whether to keep, revise, or remove the rule.
```

With the starter rules in place, the next step is to ask Codex to create the first serious notebook artifact: an investigation of what the data represents.

```{admonition} Key points
:class: key

- A prompt shapes the immediate task.
- `AGENTS.md` records standing project instructions that can load automatically in new agent sessions.
- Starter rules should respond to observed agent behavior, not abstract preferences.
- The broad prompt is useful because it shows why traceable notebook work and data-structure checks need to be explicit.
```
