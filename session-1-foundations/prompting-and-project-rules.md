# Prompting and Project Rules

A **prompt** is an instruction or message given to an AI system. It can ask a question, request an action, provide context, point the AI toward specific files, or tell it what kind of output to produce. In this lesson, prompts are the messages you type to Codex in the JupyterLab chat.

Working with a coding agent is often iterative, especially at the beginning of a project. You ask for something, observe what the agent does, and then refine either the next prompt or the standing project instructions. The first prompt does not need to be perfect, but each response gives you evidence about what the agent needs to be told more explicitly.

As the project develops, the interaction may become less repetitive. Once expectations are recorded in `AGENTS.md` and the notebook contains more context, later prompts can often be shorter because Codex has more project guidance to work from.

The wording of a prompt determines what Codex does for the immediate task. A project rules file determines how Codex should work across the project. In this lesson, we first observe what Codex does with broad and notebook-focused prompts, then turn those observations into starter rules in `AGENTS.md`.

The goal is not to prevent Codex from working quickly. The goal is to make sure its speed produces analysis that can be inspected, revised, and rerun. The workflow is:

- Try a prompt.
- Observe what Codex does.
- Identify what should be more reviewable.
- Record standing expectations in `AGENTS.md`.
- Try again with those expectations in place.

## Try one broad prompt before rules

Start with a broad request before adding project rules. This makes Codex's default behavior visible.

```{admonition} Mention Codex in JupyterLab chat
:class: warning

In the JupyterLab chat interface, start prompts with `@Codex`. The mention tells the chat which assistant should respond. If you leave it out, the message may sit in the chat without Codex answering.
```

In the Codex panel, enter:

```text
@Codex I need to do EDA on the data in my data folder. Can you investigate and tell me about it?
```

Watch what Codex does before evaluating the answer. Note whether it writes reusable notebook code, works in the terminal, summarizes in chat, creates files, or makes assumptions about the data.

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

Codex may do a lot from a vague prompt. That is useful for quick orientation, but the work may not be very traceable. Much of the analysis may happen in temporary terminal code, and the final output may be a chat summary rather than a reusable notebook artifact.

The broad prompt is useful here as a teaching demonstration, but it is not the most efficient way to work. It may spend tokens on a wide scan, a long chat summary, or analysis steps that do not become part of the notebook. The request also did not specify where the work should be recorded, ask Codex to keep the code simple, explain the data structure before interpreting trends, or leave behind a notebook section that another analyst could review.

## Try a narrower chat prompt

The broad prompt shows that Codex can move quickly, but it may also mix orientation, summary, and analysis. Before asking Codex to edit the notebook, try a narrower prompt that focuses on the data inventory and relationships:

```text
@Codex - Can you help me investigate the data in my data folder? I would like to know what the dataset or datasets are and the relationships between the items.
```

This prompt is better than the broad EDA request because it points Codex toward a specific kind of investigation. In testing, Codex identified the three datasets and explained that the title-level files connect to the aggregate table by year, month, and usage class. Your run might phrase this differently or emphasize different details.

However, the output may still be mostly a chat response. It may help orient you to the data, but it still may not leave behind a notebook artifact that another analyst can inspect and rerun.

## Try a notebook prompt

Next, ask Codex to put the investigation into the notebook:

```text
@Codex - Can you help me investigate the data in my data folder? I would like to know what the dataset or datasets are and the relationships between the items.

I have a notebook open. Please add your investigation to this notebook with code and short explanations.
```

This prompt demonstrates a capability that the chat summaries do not show: Codex can edit the notebook itself, adding code cells and explanatory text instead of only answering in the chat.

It also gives us something important to inspect: the kind of notebook code Codex might write before we give it project rules. The code may run correctly but still be difficult to review. For example, Codex may combine several analytical steps into one compact pandas expression, use helper columns without explaining them, or use technical terms before defining them.

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

- Observation: Codex answered in chat but did not leave notebook code.
- Rule: Put investigation code and short explanations in the open notebook.

Keep the rules short. You will compare them with the starter `AGENTS.md` rules in the next section.
```

## Show how AGENTS.md works

`AGENTS.md` is a project instruction file: a plain Markdown file that lives in the project folder and gives coding agents standing instructions for how to work in that project. It is not a Python file, a notebook file, or a data file. It is also not unique to this dataset; it is an [AGENTS.md convention](https://agents.md/) used by coding-agent tools to find project-specific guidance.

In this workshop, we use `AGENTS.md` to tell Codex how to handle analytics work in this repository. Once Codex has been asked to write in a notebook during a chat, it may continue doing that within the same conversation. But if notebook-based, traceable analysis is an expectation for the whole project, we do not want to retype that instruction at the start of every new chat. `AGENTS.md` gives us a place to record those standing expectations so they can be loaded automatically.

Before adding analytics workflow rules, use a temporary rule to make the mechanism visible. Create a file named `AGENTS.md` in the project root with this content:

```markdown
# AGENTS.md

## Response Style Test

Answer in haiku.
```

Ask Codex a simple question and observe whether the response changes. If the response is formatted as a haiku, the project rules are reaching the agent.

Then remove the haiku rule. The haiku test is not part of the analytics workflow; it simply shows that Codex is reading project instructions.

```{admonition} Start a new chat after changing AGENTS.md
:class: warning

After changing `AGENTS.md`, start a new Codex chat before testing the new rule. Existing chats may already have loaded the previous instructions. Reloading the chat may work in some JupyterLab setups, but starting a new chat is the clearest way to make sure Codex reads the updated file.
```

## Add first-round AGENTS.md rules

Now replace the temporary rule with a small set of non-negotiable rules for analytics work. Later, groups will add their own rules based on what they observe.

After updating `AGENTS.md`, start a new Codex chat again so the starter analytics rules are loaded for the next prompt.

Update `AGENTS.md` with the starter rules below, and fill in the Python experience level for your audience.

```markdown
# AGENTS.md

## Purpose

This project is for an AI-assisted analytics workflow.

We are using Codex to help investigate data, write Python code, create notebook explanations, and build reproducible analysis artifacts.

## Audience and Experience Level

Write explanations and code for someone with this level of Python experience:

**Python experience level:** [Fill this in]

Examples:
- new to Python
- one semester of Python
- comfortable with Python basics but new to pandas
- comfortable with pandas
- experienced with data analysis, but new to Python

## Non-Negotiable Rules

1. Inspect actual files and data before making claims.

2. Do not modify raw data files.

3. Make transformations explicit and rerunnable.

4. Do not invent column names, file names, metadata, or dataset meanings.

5. Produce code as the main artifact, not only final summaries.

6. When investigating data, create a clear notebook section with the code, outputs, and short explanations needed to support the findings. Do not add every scratch command or exploratory dead end to the notebook.

7. Before creating plots or interpreting trends, identify what one row represents, what value is being counted or aggregated, and whether the data is sampled, aggregated, or complete.

8. Favor readable, reviewable code over compact or clever code.
```

`AGENTS.md` applies to the whole project and is loaded automatically when a new agent chat starts. A prompt shapes the immediate task; `AGENTS.md` records the standing instructions you want Codex to carry into each new task in this project.

```{admonition} Exercise: Add and test your own rule
:class: exercise

Add one small rule to `AGENTS.md` that would make Codex's notebook work easier for you to review. Start a new Codex chat, then ask Codex a short question or revision request that should reveal whether the rule is being followed.

After testing, decide whether to keep, revise, or remove the rule.
```

With the starter rules in place, the next step is to ask Codex to create the first serious notebook artifact: an investigation of what the data represents.

```{admonition} Key points
:class: key

- A prompt shapes the immediate task.
- `AGENTS.md` records standing project instructions that can load automatically in new agent chats.
- Starter rules should respond to observed agent behavior, not abstract preferences.
- The broad prompt is useful because it shows why traceable notebook work and data-structure checks need to be explicit.
```
