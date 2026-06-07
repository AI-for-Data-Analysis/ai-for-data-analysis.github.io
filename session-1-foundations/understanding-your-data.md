# Understanding the Data Before Analysis

A coding agent will generate summaries and plots for any input, including data that cannot support the intended conclusion. The person doing the analysis is responsible for establishing what the data represents before interpreting results. This page covers how to direct Codex to characterize a dataset, and how to review what it returns.

## Direct the investigation with specific questions

A general request ("tell me about this data") returns whatever the agent decides is relevant. A more reliable approach is to specify the questions that characterize any dataset and require the agent to answer them from the data:

- What does one row represent?
- What value is being counted or aggregated?
- Is the data a sample, an aggregate, or a complete extract?
- How do the datasets relate to one another?
- Which dataset answers which kind of question, and what would be misleading to infer from each?

These questions are the goal of the investigation, but they do not all need to
go into the first prompt. Start with a smaller profiling task so Codex creates a
simple notebook artifact before moving into interpretation.

Ask Codex to create the first serious notebook artifact for this project:

```text
Add a simple data profile to my notebook for the data in data/. Load the files, print the first few rows, report non-null values and data types.
```

After Codex finishes, review the notebook section it created. Use the profile to
start asking what the files represent, but do not move on to plotting until the
data structure is clear.

Two parts of this prompt are doing specific work. "Don't make any plots yet"
stops the agent from producing charts before the structure is confirmed. The
request asks for basic profiling outputs rather than interpretation, which helps
keep the first notebook section compact and reviewable.

## Why this prompt is more specific

The previous lesson used a narrower prompt:

```text
Can you help me investigate the data in my data folder? I would like to know what the dataset or datasets are and the relationships between the items.
```

That prompt was better than broad EDA because it focused on data inventory and relationships. In testing, Codex identified the three datasets and explained that the title-level files connect to the aggregate table by year, month, and usage class.

However, later testing showed that asking for all of the interpretation at once
made Codex write too much code and too much explanation. We still need to answer
the data-shape questions, but it is better to build up to them from a simple
profile:

- What does one row represent?
- What is being counted?
- Is this sampled or aggregated?
- What would be misleading to infer?

The revised prompt asks only for the facts needed to begin that discussion:
files, rows, columns, data types, and non-null counts.

## Confirm the profile

Codex may add a notebook section with a compact profile for each file. Treat the
profile as a starting point, not a complete understanding of the data. The next
interpretive question is whether each file is a sample, an aggregate, or a
complete extract, because that determines which questions the file can
legitimately answer.

Review whether the notebook includes:

- files present
- row counts and shapes
- column names
- data types
- non-null counts
- a small preview of each file, if useful

After reviewing the profile, use the column names and sample rows to discuss:

- What does one row represent in each file?
- What value is being counted or aggregated?
- Which files appear sampled, aggregated, or complete?
- How might the files relate to each other?

In the checkout example, the full investigation eventually distinguishes two
title-level *sample* files from one monthly *aggregate* file, and establishes
that the samples relate to the aggregate by checkout year, month, and usage
class. The practical consequence is immediate: a question about total volume
must use the aggregate, not the samples.

In an earlier test, Codex identified:

**Digital title sample**

- `digital_checkout_title_sample_balanced_250k.csv`
- 250,000 title-month rows
- digital checkouts
- covers January 2006 through December 2025
- includes title metadata and checkout counts

**Physical title sample**

- `physical_checkout_title_sample_balanced_250k.csv`
- 250,000 title-month rows
- physical checkouts
- covers January 2006 through December 2025
- has the same schema as the digital file

**Combined monthly totals**

- `combined_checkout_totals_by_month_usageclass.csv`
- 501 monthly aggregate rows
- covers April 2005 through April 2026
- aggregated by `checkout_year`, `checkout_month`, and `usageclass`
- includes `total_checkouts`, `month_total_checkouts`, `usageclass_share`, `title_month_rows`, and `sample_rows`

Codex also tested the relationship between files:

```text
combined_checkout_totals_by_month_usageclass
  keyed by: checkout_year + checkout_month + usageclass
        |
        | matches
        v
digital_checkout_title_sample_balanced_250k
physical_checkout_title_sample_balanced_250k
  keyed by: checkoutyear + checkoutmonth + usageclass
```

It reported that the aggregate file's `sample_rows` column matched the number of rows in the title-level sample files for each month and usage class.

## Document the data for future sessions

At this point, Codex has done useful investigation that future sessions should not
need to repeat from scratch. The notebook records the analysis process, but the
basic dataset facts also belong in a durable reference file. Dataset
documentation belongs somewhere humans and agents would both expect to find it:
inside the `data/` folder.

Ask Codex to create a data README:

```text
Please create a README.md file in the data folder documenting the raw data files with enough detail that future sessions do not have to rediscover the basic dataset structure every time.
```

Review `data/README.md` before keeping it. Check that Codex did not invent
dataset meanings, overstate what the data can support, or turn sampled data into
full-population claims.

Then ask Codex to update `AGENTS.md` so future assistants know to use the data
documentation before starting new analysis:

```text
Please update AGENTS.md to tell future assistants to read data/README.md before analyzing the raw data files.
```

This is an important teaching moment. If Codex has to inspect the same files,
schemas, row counts, and relationships in every new session, the project is missing
shared memory. Once those facts have been verified, `data/README.md` can record
them so later sessions can start from known dataset orientation and spend their work
on the new question.

## Request a relationship diagram

Once the relationships are established, have the agent express them visually so they can be checked at a glance:

```{tip}
Mermaid is a text-based diagram syntax. Instead of drawing boxes and arrows by hand, you write a small block of structured text, and a renderer turns it into a visual diagram. JupyterLab can render Mermaid diagrams in notebooks, and Codex can write Mermaid syntax for common diagram types.

In this lesson, we use Mermaid to make the dataset relationships visible. This is not a separate charting library for analyzing values; it is a way to document structure.
```

Ask Codex to summarize the dataset relationships visually:

```text
Based on the investigation, add a Mermaid diagram to the notebook showing the
datasets and how they relate. It should look like an Entity Relationship diagram.
```

Review the diagram as an interpretation of the investigation, not as an automatically correct schema.

````{note}
If you want to export a Mermaid diagram outside the notebook, the official Mermaid CLI can render Mermaid text to SVG, PNG, or PDF. Mermaid CLI is a Node.js tool installed with `npm`, not a Python package. If Node.js and npm are available, one option is:

```text
npm install -g @mermaid-js/mermaid-cli
```

Then this command converts a Mermaid file to SVG:

```text
mmdc -i input.mmd -o output.svg
```

If you do not want to install it globally, see the [Mermaid CLI documentation](https://github.com/mermaid-js/mermaid-cli) for local, Docker, and other installation options.
````

### Data relationship diagram

:::{mermaid}
erDiagram
    COMBINED_MONTHLY_TOTALS {
        int checkout_year
        int checkout_month
        string usageclass
        int total_checkouts
        int month_total_checkouts
        float usageclass_share
        int title_month_rows
        int sample_rows
    }

    DIGITAL_TITLE_SAMPLE {
        string usageclass
        string checkouttype
        string materialtype
        int checkoutyear
        int checkoutmonth
        int checkouts
        string title
        string isbn
        string creator
        string subjects
        string publisher
        string publicationyear
        string sample_design
    }

    PHYSICAL_TITLE_SAMPLE {
        string usageclass
        string checkouttype
        string materialtype
        int checkoutyear
        int checkoutmonth
        int checkouts
        string title
        string isbn
        string creator
        string subjects
        string publisher
        string publicationyear
        string sample_design
    }

    COMBINED_MONTHLY_TOTALS ||--o{ DIGITAL_TITLE_SAMPLE : "monthly context by year-month-usageclass"
    COMBINED_MONTHLY_TOTALS ||--o{ PHYSICAL_TITLE_SAMPLE : "monthly context by year-month-usageclass"
:::

The diagram shows a many-to-one relationship for context only: many sampled title-month rows can correspond to one monthly aggregate row. The aggregate keys are not title identifiers.

### Discussion: Check the data model

In groups, compare the notebook investigation with the relationship diagram.

Discuss:

- Does the diagram make the sample-versus-aggregate distinction visible?
- What relationship is shown?
- What relationship is not shown?
- Which file should answer questions about total checkout volume?
- Which files should answer questions about titles, creators, subjects, or material types?

## Review the generated code

Code from a data investigation may run correctly while leaving the interpretation unclear. Reviewing the output is part of the technique, and recurring problems become additional rules for `AGENTS.md`. Three patterns are common in agent-generated analysis code:

```{admonition} Group activity: Add one rule
:class: exercise

Review the notebook section Codex created and choose one issue that would benefit from a project rule. Add one rule to `AGENTS.md`, then ask Codex to revise the investigation section so it follows the updated rules.

Compare before and after:

- Did the new rule change Codex's behavior?
- Was the rule specific enough?
- Should the rule be kept, revised, or removed?
```

Re-running the investigation after adding these rules demonstrates their effect on the output. Once the data structure is established and confirmed, the analysis can proceed.

```{admonition} Key points
:class: key

- Understanding what one row represents comes before plotting or interpreting trends.
- Sample files and aggregate files answer different kinds of questions.
- Reviewing the agent's notebook output is part of the analysis workflow, not a separate cleanup step.
```
