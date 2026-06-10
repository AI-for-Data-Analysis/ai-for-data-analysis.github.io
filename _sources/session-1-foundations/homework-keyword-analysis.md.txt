# Homework: Extend the Keyword Analysis

This homework gives you another chance to practice the Session 1 workflow on a
messy field: the `subjects` values in the Seattle Public Library title-level
sample data.

The goal is not to produce a polished report or a final subject taxonomy. The
goal is to practice using Codex to inspect data, compare approaches, and decide
what kind of method is appropriate before trusting an automated result.

## Choose one path

If you did not complete the subject-tag stretch exercise during the session,
start with {ref}`the subject-tag stretch exercise <subject-tag-stretch-exercise>`.

```text
Do the checked out materials have subject tags in any dataset? Check the raw
CSV headers and report which files include the field.
```

Then ask Codex to add a small notebook section that profiles the `subjects`
field in the digital and physical title-level samples:

```text
Add a cell to the notebook that summarizes the subjects field for the digital
and physical title-level sample files. Count the number of unique subject
values in each dataset and show a small sample of values. Keep the code simple
and explain any parsing assumptions.
```

If the result is surprising, pause before asking Codex to implement a larger
solution. Use the same method-choice prompt from the stretch exercise:

```text
The physical sample has far more unique subject values than the digital sample.
This seems like a text-cleaning or lightweight NLP problem. Do not implement
anything yet. What simpler libraries or methods could help us inspect whether
these are near-duplicates, formatting variants, or genuinely granular subjects?
```

You can also ask Codex to write a handoff prompt, then start a new thread with
`/new` and use that prompt to perform new analysis in a new notebook:

```text
Write a handoff prompt for another coding agent to investigate the subjects
field as a keyword-analysis problem. The prompt should ask the agent to profile
the field, compare raw and normalized unique counts, identify examples of
near-duplicate subject values, recommend a simple method before using an LLM,
and avoid large-scale canonicalization unless explicitly asked.
```

If you already completed the subject-tag stretch exercise, extend it by trying a
different model, reasoning setting, or method. For example, you might compare:

- a faster model and a stronger reasoning model
- a simple normalization-only approach and a fuzzy-matching approach
- RapidFuzz and scikit-learn TF-IDF
- an LLM-generated grouping proposal and a simpler string-similarity method

## Questions to investigate

Use the exercise to answer practical questions about the field:

- What does the `subjects` field appear to contain?
- How different are the raw unique counts for digital and physical samples?
- Does simple normalization reduce the number of distinct values?
- Are there obvious near-duplicates, formatting variants, or compound subject
  strings?
- Does the large physical count look like meaningful topical variety, metadata
  granularity, parsing noise, or a mixture?
- What would you trust Codex or another model to do automatically?
- What would still require human review?
