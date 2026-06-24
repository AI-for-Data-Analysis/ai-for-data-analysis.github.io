# Building Datasets with Codex

Analysis datasets rarely arrive in exactly the shape you need. A useful dataset is designed: an analyst decides what questions the data should support, what level of detail is needed, what tradeoffs are acceptable, and how the finished files should be regenerated and checked.

Codex can help with that work, but it should not replace the analyst's judgment. Use Codex to inspect sources, write retrieval scripts, create repeatable transformations, and validate outputs. Keep the analyst responsible for the questions, definitions, caveats, and claims the dataset should support.

This lesson uses the Seattle Public Library checkout data as a running example, but the workflow applies to many public datasets.

## Objectives

- explain why dataset building starts with analysis questions
- inspect a public data source before downloading it
- distinguish complete aggregate files from sampled detail files
- choose a sampling strategy based on the claims the dataset should support
- use Codex to write a reproducible dataset-building script
- define validation checks and documentation before a dataset is ready for analysis

## Start With Analysis Questions

The first dataset design decision is not how to download the data. It is what the dataset needs to help analysts answer.

For example, a checkout dataset might support questions like:

- How have digital and physical checkout totals changed over time?
- What kinds of titles, material types, or subjects appear in each checkout format?
- How did the mix of materials change across years?

Those questions require different kinds of files. Total checkout volume needs complete aggregate data. Material mix can often be explored with a sampled detail file. If the dataset tries to do everything in one file, it may become too large, too slow, or too easy to misinterpret.

```{admonition} Analyst responsibility
:class: tip

Codex can help inspect a source and write retrieval code, but the analyst has to define the questions, acceptable tradeoffs, row meaning, and claims the dataset should support.
```

## Find the Working Data Access Point

After defining the analysis need, identify how software can access the source. Public data may be available as a direct download, database export, API endpoint, bulk ZIP file, or query service.

```{admonition} What is an API?
:class: note

An **API**, or application programming interface, is a structured way for software to request information from another system. For a public dataset, an API endpoint is often a URL that returns data a script can query, filter, and save.
```

In the Seattle example, the working public endpoint was:

```text
https://data.seattle.gov/resource/tmmm-ytt6.json
```

You can find the source dataset page for Seattle Public Library checkouts [on Seattle Open Data](https://data.seattle.gov/Community-and-Culture/Checkouts-by-Title/tmmm-ytt6/about_data). The source is `tmmm-ytt6`, "Checkouts by Title." It includes both `Digital` and `Physical` values in a `usageclass` field, which made it a good fit for analyzing changing checkout patterns.

```{admonition} Endpoint note
:class: note

Some data portals expose more than one URL pattern. The original Seattle link used the `api/v3/views/.../query.json` pattern. For unauthenticated retrieval, the script used the public Socrata SODA resource endpoint instead: `https://data.seattle.gov/resource/tmmm-ytt6.json`. Confirm the working public endpoint before asking Codex to write retrieval code.
```

## Inspect the Source Before Downloading

Before pulling a large dataset, ask Codex to inspect what the source represents. The important questions are structural:

- What does one source row represent?
- Is the source already aggregated, or is it row-level event data?
- What time span does it cover?
- Which fields are available for filtering, grouping, or sorting?
- How large is the source?
- Can the endpoint support server-side filters or grouped queries?

In the Seattle source, one row is not one checkout. The source is already aggregated: one row represents a title/material/usage-class/month combination, with a `checkouts` count.

That row meaning changes the analysis. If a row has `checkouts = 47`, it is a title-month record summarizing 47 checkouts for that combination. Treating that row as one checkout would undercount activity and distort any interpretation of volume.

## Design the Output Files

Once the source is understood, design the smaller files analysts will actually use. This is where the analysis questions become file contracts. You can work with Codex to establish this based on the available data and questions you want to ask.

| Question type | Example | Useful output file |
| --- | --- | --- |
| Volume | How did digital and physical checkout totals change over time? | Complete aggregate totals |
| Composition | What kinds of titles, material types, or subjects appear in each checkout format? | Sampled detail records |

For the Seattle data, this led to a three-file design:

```text
seattle-public-library/
  combined_checkout_totals_by_month_usageclass.csv
  digital_checkout_title_sample_balanced_250k.csv
  physical_checkout_title_sample_balanced_250k.csv
  README.md
```

The totals file preserves complete monthly counts by `usageclass`. The two sample files provide manageable title/month records for digital and physical exploration. The sample files have the same structure because they come from the same source and were split by `usageclass` after retrieval.

## Choose a Sampling Strategy

Sampling is not just a file-size trick. A sampling strategy changes what claims analysts can make.

Sampling was necessary for the Seattle title/month records because the source contained far more rows than we could reasonably package in a normal repository or ask analysts to load during a short exercise. The design keeps the monthly totals complete, because those files are small after aggregation. It samples the title-level detail records, because that is the part of the source that is too large to distribute directly.

Several sampling strategies could support different goals:

- **Most recent rows**: useful for current-state inspection, weak for historical comparisons.
- **Simple fixed-size sample**: easy to create, but may overrepresent high-volume periods or common groups.
- **Proportional sample**: useful when the sample should resemble the full source population.
- **Balanced sample by year**: useful when analysts need enough rows from each year for comparison.
- **Separate balanced samples by group**: useful when comparing groups that have very different source volumes.

For the Seattle data, the final choice was a balanced sample by year and usage class:

```text
2006-2025
20 complete years
250,000 Digital rows
250,000 Physical rows
12,500 rows per year per usageclass
```

The sample is balanced at the year and usage-class level, not at the month level. Each year gets 12,500 Digital rows and 12,500 Physical rows. Within that year, months with more source rows get more sampled rows than months with fewer source rows. For example, if July has twice as many title/month records as February for Physical checkouts in a given year, July receives about twice as many rows in that year's Physical sample.

The script also makes the sample method repeatable. Running the script again should apply the same year range, group definitions, and sampling rules, rather than creating an undocumented one-off extract.

Balanced sampling fit this workflow because analysts can compare patterns across years. A proportional sample would represent the overall source population more directly, but high-volume years would dominate the sample and lower-volume years would have fewer rows for comparison. The complete totals file preserves real volume, so the sample can focus on composition.

```{admonition} Sampling tradeoff
:class: note

A balanced-by-year sample is useful for comparing composition across years. A proportional sample is useful for estimating the overall source population. The right choice depends on the question the dataset should support.
```

## Ask Codex for a Reproducible Builder

Once the dataset design is clear, ask Codex for a script, not a one-time download. The script is the method. It should show the source endpoint, retrieval choices, filters, sampling design, output paths, and validation checks.

The key prompt is not simply:

```text
Download this data.
```

A better prompt is:

```text
Write a reproducible script that creates these analysis files from this public
endpoint. Use the approved file design, make the sampling method repeatable,
write partial outputs safely, and validate the final row counts.
```

The script should make the retrieval method visible without requiring analysts to repeat manual download steps. For the Seattle dataset, that meant querying the public endpoint, creating the approved aggregate and sample files, and writing outputs that matched the dataset design.

```{admonition} Why write a script?
:class: tip

A script turns dataset retrieval into a reviewable method. Reviewers can inspect the source URL, retrieval choices, sampling design, output paths, retry behavior, and validation checks.
```

## Prompt Sequence

Do not ask Codex to inspect the source, design the dataset, and build the script all at once. Break the work into stages so you can review the decisions before Codex writes code.

First, ask Codex to inspect the source:

```text
I want to build a reproducible analysis dataset from [SOURCE].

Inspect the source access pattern and metadata. Do not download the full dataset
yet. Tell me:
- what the source appears to contain
- what one row represents
- whether the source is row-level or already aggregated
- what fields are available for filtering or grouping
- how large the source appears to be
```

Then ask for a dataset design:

```text
Using what you found, recommend a dataset design for these analysis questions:
- [QUESTION 1]
- [QUESTION 2]
- [QUESTION 3]
```

After you approve the design, ask for the builder script:

```text
Write a script that can regenerate the approved files.
The script should use a repeatable retrieval method create a short README to accompany the script.
```

This sequence separates source inspection, dataset design, and implementation. 

## Key Points

```{admonition} Key points
:class: key

- Dataset building starts with analysis questions, not downloading.
- Public data retrieval starts with source inspection.
- Row meaning determines what the dataset can and cannot support.
- Complete aggregate files and sampled detail files serve different purposes.
- Sampling strategy changes what claims analysts can make.
- A reproducible script makes the dataset method inspectable and rerunnable.
- Long-running downloads need partial-file handling, retries, and validation.
- Minimal documentation should explain source, files, row meaning, sampling, and retrieval method.
```
