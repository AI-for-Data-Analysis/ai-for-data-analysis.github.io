# Prompting and Project Rules

The wording of a prompt determines what Codex produces and what remains afterward. In this lesson, we'll contrast a broad prompt with a project rules file that sets standing expectations.

## Run an unconstrained prompt

In the Codex panel, enter:

```text
I need to do EDA on the data in my data folder. Can you investigate and tell me about it?
```

Codex inspects the project and locates the three files in `data/`:

```text
combined_checkout_totals_by_month_usageclass.csv
digital_checkout_title_sample_balanced_250k.csv
physical_checkout_title_sample_balanced_250k.csv
```

It reads each file and computes row counts, column types, date ranges, category counts, and top titles, then returns a summary. The summary correctly notes that physical checkouts were higher through 2019, that digital checkouts overtook physical checkouts around 2020, and that two of the files are samples rather than complete extracts.

## Result

Most of this work runs in a temporary terminal and is not written to the notebook. The notebook remains empty, so the conclusions cannot be reproduced or reviewed. The output is a correct summary with no supporting artifact.

A broad prompt is acceptable for orientation, but the request did not specify where the work should be recorded. A prompt that directs the work into the notebook with readable code produces a reproducible result instead.

## Define project rules in AGENTS.md

Rather than restating these expectations in every prompt, record them once in a file Codex reads for every task. Create a file named `AGENTS.md` in the project root with the following rules:

```markdown
# AGENTS.md

## Non-Negotiable Rules

1. Inspect actual files and data before making claims.
2. Do not modify raw data files.
3. Make transformations explicit and rerunnable.
4. Do not invent column names, file names, metadata, or dataset meanings.
5. Produce code as the main artifact, not only final summaries.
6. When investigating data, build a clear notebook section with the code,
   outputs, and short explanations that support the findings — without dumping
   every scratch command into the notebook.
7. Before plotting or interpreting trends, state what one row represents, what
   value is being counted, and whether the data is sampled, aggregated, or complete.
8. Favor readable, reviewable code over compact or clever code.
```

`AGENTS.md` applies to the whole project. A prompt shapes a single task; `AGENTS.md` shapes every task.

Each rule corresponds to a behavior observed in the broad prompt above: Codex summarized before producing an artifact (rule 5), worked outside the notebook (rule 6), and proceeded toward results before establishing what the data represented (rule 7). Rules are derived from observed behavior rather than written in advance.

## Verify the rules are applied

Confirm that Codex reads `AGENTS.md` before relying on it. Add a temporary rule:

```markdown
## Response Style Test

Answer in haiku.
```

Ask Codex any question. If the response is formatted as a haiku, the project rules are reaching the agent. Remove the temporary rule before continuing.

With the rules in place, the next step is to establish what the data represents before analyzing it.
