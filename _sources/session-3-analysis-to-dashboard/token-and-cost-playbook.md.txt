# Token And Cost Playbook

## Why This Belongs In Analytics Work

Token and cost control is a workflow skill, not only a multi-agent concern. Strong analysts decide when AI is needed and when deterministic programs are better.

## Learning Objectives

- Apply a practical policy for AI vs deterministic work.
- Choose model tier based on task complexity.
- Reduce token usage without reducing analysis quality.

## Default Policy

1. Deterministic first

- Use Python/SQL/shell for file listing, schema checks, joins, aggregation, validation, and chart generation.

2. AI for ambiguity

- Use AI for planning, interpretation, critique, and edge-case reasoning.

3. Escalate model capability only when needed

- Start with lower-cost models for routine tasks.
- Move to higher-capability models when quality is not sufficient.

## Model Selection Heuristic

- Lower-cost model: file exploration, formatting, boilerplate, simple refactors.
- Higher-capability model: analysis design, tricky debugging, reasoning about assumptions and limitations.

## Token Reduction Tactics

- Ask for a plan before requesting full code.
- Share schema summaries and small samples instead of full data.
- Scope prompts to one decision at a time.
- Reuse scripts/functions; avoid regenerating the same code repeatedly.
- Persist stable logic in files and call those files directly.

## Practical Monitoring Habit

At each milestone, record:

- Task objective
- Model used
- Approximate token/cost usage
- Whether a deterministic alternative could replace part of the work

Use this log during retrospectives to improve team workflow in later sessions.

## Reflection Prompts

- Which step today should have been deterministic instead of AI-assisted?
- Where did a larger model materially improve quality?
- Where did it not?
