# Understanding the Data Before Analysis

A coding agent will generate summaries and plots for any input, including data that cannot support the intended conclusion. The analyst is responsible for establishing what the data represents before any analysis. This page covers how to direct Codex to characterize a dataset, and how to review what it returns.

## Direct the investigation with specific questions

A general request ("tell me about this data") returns whatever the agent decides is relevant. A more reliable approach is to specify the questions that characterize any dataset and require the agent to answer them from the data:

- What does one row represent?
- What value is being counted or aggregated?
- Is the data a sample, an aggregate, or a complete extract?
- How do the datasets relate to one another?
- Which dataset answers which kind of question, and what would be misleading to infer from each?

Frame the prompt around these questions, and constrain where the work goes and how far it proceeds:

Ask Codex to create the first serious notebook artifact for this project:

```text
Help me investigate the data in my data folder. I want to know what datasets
are present, what one row represents in each, what values are being counted,
whether each dataset is sampled or aggregated, and how the datasets relate to
each other. Add your investigation as traceable, readable code in my open
notebook. Keep it simple, and don't make any plots yet.
```

After Codex finishes, review the notebook section it created. Do not move on to plotting until the data structure is clear.

Two parts of this prompt are doing specific work. "Don't make any plots yet" stops the agent from producing charts before the structure is confirmed. The instruction to work in the notebook is not strictly necessary here, because it is already a project rule — but the request still names the questions explicitly, since these are particular to the task rather than standing expectations.

## Confirm what the agent reports

The agent will add a notebook section answering each question. Treat its answers as claims to confirm, not conclusions to accept. The distinction that matters most is **sample versus aggregate**, because it determines which questions a dataset can legitimately answer: a sampled file describes patterns, while an aggregate file reports totals.

In the checkout example, the investigation distinguishes two title-level *sample* files from one monthly *aggregate* file, and establishes that the samples relate to the aggregate by checkout year, month, and usage class. The practical consequence is immediate — a question about total volume must use the aggregate, not the samples — and that conclusion comes directly from having characterized the data first.

## Request a relationship diagram

Once the relationships are established, have the agent express them visually so they can be checked at a glance:

Ask Codex to summarize the dataset relationships visually:

```text
Based on the investigation, add a Mermaid diagram to the notebook showing the
datasets and how they relate. Make clear which file is the monthly aggregate and
which are title-level samples.
```

Review the diagram as an interpretation of the investigation, not as an automatically correct schema.

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

**Multiple steps combined in one expression.** A single statement may group, aggregate, relabel, concatenate datasets, reset the index, and select columns at once, which is difficult to review.

```markdown
- Use named intermediate variables when they make analytical steps easier to inspect.
```

**Derived columns without explanation.** An agent may add a display or helper column — for example, a representative value selected from each group — that is indistinguishable in the output from a primary field.

```markdown
- When creating helper columns, matching keys, or display values, explain how they should be read.
```

**Correct but unclear terminology.** An agent may use precise but unfamiliar terms (for instance, "grain" for what one row represents) without defining them.

```markdown
- Prefer plain phrasing like "what one row represents" before introducing terms like "grain."
```

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
