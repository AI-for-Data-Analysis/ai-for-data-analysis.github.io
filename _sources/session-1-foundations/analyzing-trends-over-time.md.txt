# Planning and Running an Analysis

This page applies the preceding steps to a complete analysis question:

> How have physical and digital checkouts changed over time?

It also shows how to use Codex for planning before implementation when the next analysis might require a library or visualization approach we have not already chosen.

## Select the appropriate file

Determine which file can answer the question before writing a prompt. The dataset contains two title-level samples and one monthly aggregate. Overall borrowing volume over time is a question about totals, so it must use the 501-row aggregate file. The 250,000-row sample files describe patterns and do not represent total volume.

This is the purpose of the previous investigation: knowing the structure of the data determines which file is correct. State the chosen dataset in the prompt.

## Run the analysis

In the Codex terminal, enter:

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

````{admonition} Ask for a change on the chart
:class: exercise

Choose something you would like to see changed on the chart. This could have to do with font size, color, or style.

Ask Codex to change your chart. Continue prompting until you are satisfied with the plot style.
````

## Review checklist

Review the output against the following:

- Did it use the aggregate file rather than a sample file?
- Did it state what one row represents before interpreting the data?
- Did it account for the partial 2026 year?
- Does each stated result correspond to specific code and output?

## Plan a new visualization before implementing

Not every prompt needs to ask Codex to make changes immediately. When the next step involves choosing an approach, a library, or a visualization type, use Codex as a planning partner first.

> Does the data show any seasonal patterns for checkouts over time?

This question still uses the monthly aggregate file, but the best visualization is less obvious than a basic trend line. A heatmap, faceted chart, small multiples, or an interactive chart might each work. Before installing anything or adding notebook cells, ask Codex to discuss possible approaches:

```text
I'd like to discuss investigating checkout seasonality over time for checkouts. I'm curious if
there is any time of year where checkouts occur more or less often. How might we do that?
```

A key phrase used here is "I'd like to discuss...". 
This will keep Codex from acting until you have discussed the topic and greenlighted an action.

Review the options before moving forward. The useful output is not just the name
of a chart type; it should explain tradeoffs such as readability, complexity,
whether the chart will render reliably in the notebook, and whether the code
will be easy to review.

If the recommendation is appropriate, then ask Codex to implement the chosen approach:

```text
Use the recommended approach to add a simple, readable notebook section
showing monthly checkout seasonality by usage class. Explain what the
visualization shows and include one caveat.
```

This demonstrates a different prompting pattern: discuss and decide first, then implement. That pattern is useful whenever the analysis goal is clear but the method is still uncertain.

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

(subject-tag-stretch-exercise)=
````{admonition} Stretch exercise: Treat subject tags as a text-cleaning problem
:class: exercise

The title-level sample files include a `subjects` field. This field can look
simple at first, but it is a useful stretch case because a small profiling
question can turn into a text-cleaning and interpretation problem.

Start by asking Codex a narrow verification question:

```text
Do the checked out materials have subject tags in any dataset? Check the raw
CSV headers and report which files include the field.
```

If the field exists, ask Codex to add a short notebook section:

```text
Add a cell to the notebook that summarizes the subjects field for the digital
and physical title-level sample files. Count the number of unique subject
values in each dataset and show a small sample of values. Keep the code simple
and explain any parsing assumptions.
```

Review the result carefully. In testing, the digital and physical samples had
very different unique subject counts. That difference should not be interpreted
immediately as "physical has many more meaningful topics." It may reflect
metadata practices, compound subject strings, punctuation, separators,
granularity, or the way the field was split.

Use the surprising result to discuss method choice before implementing a larger
analysis:

```text
The physical sample has far more unique subject values than the digital sample.
This seems like a text-cleaning or lightweight NLP problem. Do not implement
anything yet. What simpler libraries or methods could help us inspect whether
these are near-duplicates, formatting variants, or genuinely granular subjects?
```

The useful teaching point is the decision process. A library such as RapidFuzz
can score string similarity, and scikit-learn can support TF-IDF comparisons or
clustering, but neither one automatically solves the interpretation problem.
The analyst still needs to decide how subjects should be parsed, normalized,
reviewed, and possibly grouped.

You can have the agent write a handoff prompt for a future agent:

```text
Write a handoff prompt for another coding agent to investigate the subjects
field as a keyword-analysis problem. The prompt should ask the agent to profile
the field, compare raw and normalized unique counts, identify examples of
near-duplicate subject values, recommend a simple method before using an LLM,
and avoid large-scale canonicalization unless explicitly asked.
```

If you start a new thread with `/new`, you can use this prompt to perform new analysis in a new notebook. 
(You can also keep going with the same agent, this just demonstrates hand off)

````

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
- Codex can help compare analysis approaches before writing code or installing anything.
- A coding agent can do much of the analytical work, but the person interpreting the results must confirm that the output is understandable, reviewable, and traceable.
```
