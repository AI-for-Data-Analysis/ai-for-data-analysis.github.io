# Agent Skills

In Session 1, you used prompts and `AGENTS.md` to shape how Codex worked in one project. In the previous lesson, you saw that the working file format also shapes the agent's behavior.

Skills solve a related problem: repeated instructions should not live only in the conversation.

When the same guidance appears in many prompts, that guidance may belong in a skill.

## Objectives

- distinguish prompts, `AGENTS.md`, and skills
- describe the parts of a skill, including `SKILL.md` and optional supporting files
- explain progressive disclosure for skill loading
- identify where skills can be stored or installed from
- evaluate whether a skill changes agent behavior in the intended way

## The Problem Skills Solve

Suppose a project repeatedly needs figures for analysis presentations:

```text
Use Duke colors. Make the figure readable on a PowerPoint slide. Use large text
and markers. Do not put a title on the figure. Save the figure as a high-quality
PNG.
```

The instruction can work in one prompt, but repeating it manually creates several problems:

- You may forget part of the instruction.
- Codex may follow it differently across sessions.
- The instruction takes up prompt space.
- A collaborator may not know the convention.
- The project has no reusable record of what "a good figure" means.

A skill records that repeated workflow in a reusable instruction file.

## Prompt, AGENTS.md, or Skill?

These three instruction types do different jobs:

| Instruction type | Best use |
| --- | --- |
| Prompt | The immediate task: "Analyze this file" or "revise this chart." |
| `AGENTS.md` | Standing rules for one project: audience, file locations, raw-data rules, review expectations. |
| Skill | Reusable workflow guidance for a type of task across projects. |

In Session 1, `AGENTS.md` told Codex how to work in the checkout-analysis project. A skill is more portable. It can define a reusable method for Duke-style figures, dashboard accessibility review, pedagogical explanations, or recurring data-validation checks.

## What Is a Skill?

An agent skill is a reusable instruction set that extends an AI agent with specialized knowledge or a procedural workflow. In practice, a skill is usually a folder or repository containing:

- a `SKILL.md` file
- optional supporting files, such as templates, examples, scripts, or reference material

The core of a skill is `SKILL.md`. Supporting files are optional. For example, Jessica's [pedagogy skill](https://gitlab.oit.duke.edu/jn242/skills/-/blob/main/skills/pedagogy/SKILL.md?ref_type=heads) starts with metadata that lets an agent discover when the skill applies, followed by instructions for how to teach:

```markdown
---
name: pedagogy
description: "Use this skill when creating educational content that needs to genuinely teach, not just inform."
---

# Pedagogy Skill

Principles for creating educational content that genuinely teaches.

## Core Philosophy

The goal is **understanding**, not information transfer.
```

The metadata is part of the skill interface. The name and description support discovery; the body of the file gives the agent the workflow to follow after the skill is activated.

A minimal skill might look like this:

```markdown
---
name: duke-analysis-figures
description: Use this skill when creating figures for Duke analytics presentations.
---

# Duke Analysis Figures

Create figures that are readable in presentation settings.

## Rules

- Use Duke Navy `#012169` and Duke Royal Blue `#00539B` as primary colors.
- Use Copper `#C84E00` or Persimmon `#E89923` only for emphasis.
- Use large axis labels and tick labels.
- Do not add chart titles unless the user asks.
- Save figures as high-resolution PNG files.
- Prefer clear labels and direct annotations over dense legends.
```

That is enough to define a reusable standard. More advanced skills can include scripts, templates, image assets, or examples.

## How Skills Are Loaded

Agents do not need to load every full skill into context all the time. Skills use a pattern called **progressive disclosure**. The [Agent Skills documentation](https://agentskills.io/home) describes this in three stages:

- **Discovery**: the agent sees the name and description, enough to know when the skill might be relevant.
- **Activation**: when a task matches the skill, the agent reads the full `SKILL.md`.
- **Execution**: the agent follows the instructions and may load supporting files or run bundled scripts if the skill calls for them.

The boundary matters. A skill works because the agent can discover it, read it when relevant, and apply the written instructions to the current task.

You can also explicitly attach a skill in a prompt:

```text
$pedagogy Draft this lesson so students understand why the workflow works, not
just what commands to run.
```

The `$skill_name` pattern tells the agent which reusable instruction set should shape the response.

## Where Skills Live

Codex and other tools look for skills in well-known locations. Common locations include:

| Scope | Example locations |
| --- | --- |
| Global skills | `~/.codex/skills`, `~/.agents/skills` |
| Project skills | `.codex/skills`, `.agents/skills` |

Global skills are available across projects. Project skills travel with a repository and are useful when everyone working in the project should share the same workflow guidance.

Use a project skill when the instruction is part of how this project works. Use a global skill when the instruction is part of how you personally work across many projects.

## Skill Effects

The same prompt can produce different outputs when different skills are active. In the deck example below, an undergraduate project used skills to steer an AI art system connected to a physical drawing device. The prompt stayed the same, but the skill changed the method and style.

```{figure} ../images/session-2/session-2-slide-17.png
:alt: Three line-art outputs produced from the same prompt using different skills: line art, algorithmic art, and Bauhaus art
:width: 100%

Skills can make the agent apply a specified method to the same request.
```

For analytics, the difference may be less visually dramatic but operationally useful. A skill can direct Codex to:

- always profile data before modeling
- use a specific chart style
- write beginner-readable pandas code
- validate dashboard-ready output files
- check accessibility issues in a chart
- produce a stakeholder-ready summary format

The key test is whether the skill changes observable behavior.

## Skills Repositories

Skills can be shared through Git repositories. These collections provide examples
to inspect, install, or adapt:

- [Duke AI skills collection](https://gitlab.oit.duke.edu/ai-tech/skills/)
- [OpenAI skills collection](https://github.com/openai/skills)
- [Anthropic skills collection](https://github.com/anthropics/skills)

Review a skill before using it. A skill can include instructions, scripts,
templates, and other supporting files, so it should be treated as project code
rather than only as prompt text.

## Installing or Creating Skills

Some skills can be installed from a Git repository with `npx skills`:

```{admonition} If `npx` is missing
:class: tip

`npx` is included with modern versions of `npm`. Check that Node.js, `npm`, and
`npx` are available:

```bash
node --version
npm --version
npx --version
```

If one of these commands is missing, install Node.js and `npm` using the setup
instructions for your operating system, then run the checks again.
```

```bash
npx skills install SKILL_REPO
```

If a repository contains multiple skills, specify the one you want:

```bash
npx skills install SKILL_REPO --skill SKILL_NAME
```

You can also ask Codex to help create a skill with `$skill-creator`:

```text
$skill-creator I want to create a skill for producing figures when I'm doing
data analysis. I want to use the Duke color scheme for my figures, and I want
the output to be high quality and appropriate for PowerPoint. The text and
markers should be large and readable, and figures should not have titles.
```

That prompt describes the reusable workflow standard that the skill should capture.

## Test a Skill Like an Analyst

Evaluate a skill before relying on it.

Use a before-and-after comparison:

1. Ask Codex to perform the task without the skill.
2. Save or inspect the output.
3. Ask Codex to perform a similar task with the skill.
4. Compare the outputs against the behavior the skill was supposed to produce.
5. Revise the skill if the difference is not clear enough.

For the Duke figure example, you might check:

- Are the colors appropriate?
- Is the text readable on a slide?
- Are markers and lines large enough?
- Did the figure avoid unnecessary titles?
- Was the output saved at useful resolution?
- Would the figure work in a dashboard presentation?

This evaluation checks whether the written skill produces the intended behavior.

```{admonition} Key points
:class: key

- Prompts guide the immediate task.
- `AGENTS.md` guides one project.
- Skills guide reusable workflows across tasks or projects.
- A skill is usually `SKILL.md` plus optional supporting files.
- Skills are loaded through discovery, activation, and execution.
- Test a skill by comparing behavior before and after using it.
```
