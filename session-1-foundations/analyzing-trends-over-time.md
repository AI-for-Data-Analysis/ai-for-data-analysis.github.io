# Analyzing Checkout Trends Over Time

This page applies the preceding steps to a complete question:

> How have physical and digital checkouts changed over time?

## Select the appropriate file

Determine which file can answer the question before writing a prompt. The dataset contains two title-level samples and one monthly aggregate. Overall borrowing volume over time is a question about totals, so it must use the 501-row aggregate file. The 250,000-row sample files describe patterns and do not represent total volume.

This is the purpose of the previous investigation: knowing the structure of the data determines which file is correct. State the chosen dataset in the prompt.

## Run the analysis

In the Codex panel, enter:

```text
Using the monthly aggregate checkout dataset, analyze how physical and digital
checkouts changed over time. Add traceable code and short explanations to the
notebook. Include annual totals, a trend chart, and a note about any partial
years.
```

When Codex finishes, use the review checklist below before accepting the result.

The prompt does not restate the requirements defined in `AGENTS.md`, such as readable code and notebook output; those apply automatically. It specifies only what is particular to this task: the dataset, the required outputs, and the caveat to address.

## Expected output

Codex adds annual totals split by physical and digital, a trend chart across the full range, and the digital share over time. The data shows physical checkouts higher in the early years, digital checkouts increasing over time, and a crossover around 2020.

The aggregate file runs through April 2026, so the final year is incomplete. If 2026 is summed and charted alongside full years, it will appear as a sharp decline because four months are compared against twelve. The analysis must flag the partial year. Confirm that Codex did so; if it did not, instruct it to add the note.

## Review checklist

Review the output against the following:

- Did it use the aggregate file rather than a sample file?
- Did it state what one row represents before interpreting the data?
- Did it account for the partial 2026 year?
- Does each stated result correspond to specific code and output?

## Apply the workflow to the sample data

The aggregate file answers questions about totals. The title-level sample files answer more granular questions about titles, subjects, material types, and publishers. Select one such question and apply the same workflow:

```text
What material types dominate the digital vs physical samples?
Which subjects appear most often in each sample?
What titles or creators appear in both the digital and physical samples?
How does publication year differ between digital and physical samples?
```

Use a prompt that carries the same requirements:

````{admonition} Group activity: Investigate a sample-data question
:class: exercise

Choose one granular question about the title-level sample files, or write your own. Use this prompt template:

```text
Help me investigate this question: [QUESTION]. Use the title-level sample
files. Before analyzing, state what one row represents and what is being
counted. Add traceable, readable code to the notebook with short explanations.
End with one finding and one caveat.
```

Prepare a short share-out with:

- the question your group investigated
- the dataset used
- what one row represents
- the code or output that supports the finding
- one finding
- one caveat or uncertainty
- one thing Codex did well or poorly
````

These files are samples, not the complete collection. A finding describes the sample; any statement about the full collection is an inference. State which one applies.

## Summary

The workflow completes one full iteration of the cycle: an initial broad prompt produced results without an artifact; reviewing the output produced project rules; the data structure was established before analysis; and the correct file was used to answer the question with traceable code.

```text
Run a prompt.
Review what Codex did.
Define rules early.
Apply the rules while continuing the analysis.
Add rules as further issues appear.
Compare results before and after, and continue.
```

```{admonition} Key points
:class: key

- The aggregate file answers questions about total checkout volume.
- The title-level sample files answer more granular questions about titles, subjects, material types, and publishers.
- A coding agent can do much of the analytical work, but the analyst must confirm that the output is understandable, reviewable, and traceable.
```
