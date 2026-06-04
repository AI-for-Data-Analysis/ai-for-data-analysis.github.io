# Prompting Planning Context

## Why This Matters

AI assistant quality depends on problem framing and context quality. Analysts should request plans first, then code, then validation.

## Learning Objectives

- Write prompts that produce useful analytics outputs.
- Use a consistent sequence: plan -> implementation -> validation -> critique.
- Manage context so the assistant has grain, constraints, and expected outputs.

## Prompt Structure for Analysts

Include:

- Objective: what decision or question the analysis supports
- Data context: files, grain, known joins, caveats
- Constraints: tool/language, runtime limits, file outputs
- Validation: required checks and success criteria

## Suggested Prompt Sequence

1. Ask for a plan.
2. Ask for implementation from that plan.
3. Ask for validation and edge-case checks.
4. Ask for critique and failure modes.

## Example: Plan Prompt

```text
Goal: analyze daily building activity trends for a tutorial.
Data: building_activity_by_day_affiliation.csv and building_activity_by_day_ssid.csv.
Give me a step-by-step analysis plan with joins, checks, and outputs.
Do not write code yet.
```

## Example: Validation Prompt

```text
Review this analysis logic as if you are a strict code reviewer.
Identify risks, missing checks, and assumptions that could break conclusions.
```

## Context Hygiene Rules

- Provide only necessary files and schema details.
- Restate key assumptions in each major prompt.
- Ask for explicit unknowns instead of implicit guesses.
- Keep outputs file-based when moving to production mode.
