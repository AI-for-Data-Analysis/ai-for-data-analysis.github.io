# Discovery Mode

## Why This Comes First

Analysts need a fast way to learn what data can and cannot answer before locking into production code. Discovery mode is that phase: conversational, exploratory, and hypothesis-driven.

## Guiding Questions

- What can this dataset help us answer?
- What assumptions are we making too early?
- What should we test before claiming a result?

## Learning Objectives

- Distinguish discovery mode from production mode.
- Use AI assistants to generate candidate questions and quick checks.
- Record findings that will transfer into reproducible analysis.

## Workflow Pattern

1. Start with plain-language questions.
2. Ask the assistant to propose 3-5 testable hypotheses.
3. Ask for quick schema/column sanity checks.
4. Keep a short log of assumptions and unknowns.

## Discovery Prompt Starters

```text
We are in discovery mode. Help me understand what this dataset is about.
First, propose 5 analyst questions this data might answer.
Then list what columns or joins each question would require.
```

```text
Based on these CSV headers, what are the likely grains of each table?
Where are likely join keys, and where are there key mismatches?
```

```text
What could go wrong if we treat these counts as comparable across files?
Give me a validation checklist before analysis.
```

## Common Pitfalls

- Treating assistant guesses as facts without checks.
- Skipping grain definition (row-level meaning).
- Overcommitting to one question before understanding data limitations.

## Exit Criteria for Discovery Mode

Switch to production mode when:

- One primary analysis question is selected.
- Required fields and joins are identified.
- At least three validation checks are defined.
