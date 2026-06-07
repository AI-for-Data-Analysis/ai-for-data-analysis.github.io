Session 1: Foundations for AI-Assisted Analytics Work
=====================================================

This session uses Codex, a coding agent, to investigate a dataset and answer a
question about it while keeping the analysis **understandable, reviewable, and
traceable**. The example dataset is two decades of library checkout records.

The session covers how prompts and an ``AGENTS.md`` rules file determine what
Codex produces, how to establish what the data represents before analyzing it,
how to produce a trend analysis in which each result is traceable to its code,
and how to manage context so agent sessions stay focused.

.. admonition:: The iterative cycle
   :class: note

   Run a prompt. Review what Codex did. Record a rule to correct it. Run again,
   and continue into the analysis.

Complete the environment and assistant setup before starting:
`Complete setup <../setup.html>`_

.. csv-table::
   :file: ../csv_tables/session_1_foundations_pages.csv
   :header-rows: 1

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   coding-agents-for-analytics
   prompting-and-project-rules
   understanding-your-data
   analyzing-trends-over-time
