from pathlib import Path

SECTIONS = [{"include": True, "lessons": ["discovery-mode", "prompting-planning-context", "environments-version-control", "mini-analytics-challenge"], "slug": "session-1-foundations", "title": "Session 1: Foundations for AI-Assisted Analytics Work"}, {"include": True, "lessons": ["skills-overview", "create-or-refine-eda-skill", "skill-testing-and-iteration"], "slug": "session-2-reusable-skills", "title": "Session 2: Reusable Skills for Analytics Work"}, {"include": True, "lessons": ["multi-agent-workflows", "analysis-validation-patterns", "dashboard-build-sprint"], "slug": "session-3-analysis-to-dashboard", "title": "Session 3: From Analysis to Dashboard"}, {"include": True, "lessons": ["presentation-structure", "reflection-and-next-steps", "capstone-retrospective"], "slug": "session-4-presentations-reflection", "title": "Session 4: Dashboard Presentations and Reflection"}]
INCLUDE_CSV_TABLES = True
SCAFFOLD_LESSONS = True
LESSON_STUB_STYLE = "question-driven"


def title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def lesson_body(section_title: str, lesson_slug: str, lesson_title: str) -> str:
    if LESSON_STUB_STYLE == "minimal":
        return (
            f"# {lesson_title}\n\n"
            f"Content for `{section_title}` / `{lesson_slug}`.\n"
        )

    if LESSON_STUB_STYLE == "narrative":
        return (
            f"# {lesson_title}\n\n"
            "## Overview\n\n"
            f"This lesson introduces {lesson_title.lower()} in the context of {section_title}.\n\n"
            "## Why It Matters\n\n"
            "Explain what learners should be able to do after reading this lesson.\n\n"
            "## Walkthrough\n\n"
            "Add examples, configuration snippets, and commentary here.\n\n"
            "## Key Takeaways\n\n"
            "- Main concept 1\n"
            "- Main concept 2\n"
            "- Main concept 3\n"
        )

    return (
        f"# {lesson_title}\n\n"
        "## Guiding Questions\n\n"
        f"- What is {lesson_title.lower()}?\n"
        f"- How does {lesson_title.lower()} fit into {section_title}?\n"
        "- What tradeoffs should a learner know?\n\n"
        "## Learning Objectives\n\n"
        "- Understand the core concept.\n"
        "- Apply the concept in a real workflow.\n"
        "- Identify common mistakes and how to avoid them.\n"
    )


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_section_index(section: dict) -> str:
    title = section["title"]
    slug = section["slug"]
    lessons = section.get("lessons", [])

    lines = [
        title,
        "=" * len(title),
        "",
        f"This section covers {title.lower()}.",
        "",
    ]

    if INCLUDE_CSV_TABLES:
        lines.extend(
            [
                ".. csv-table::",
                f"  :file: ../csv_tables/{slug.replace('-', '_')}_pages.csv",
                "  :header-rows: 1",
                "",
            ]
        )

    lines.extend([".. toctree::", "   :maxdepth: 1", "   :hidden:", "", "   self"])

    for lesson in lessons:
        lines.append(f"   {lesson}")

    lines.append("")
    return "\n".join(lines)


def build_section_csv(section: dict) -> str:
    lessons = section.get("lessons", [])
    rows = ["Page,Questions,Objectives"]
    for lesson in lessons:
        lesson_title = title_from_slug(lesson)
        rows.append(
            f"`{lesson_title} <{lesson}.html>`_,\"* What is {lesson_title.lower()}?\",\"* Understand {lesson_title.lower()}.\""
        )
    return "\n".join(rows) + "\n"


def main() -> None:
    csv_dir = Path("csv_tables")
    if INCLUDE_CSV_TABLES:
        csv_dir.mkdir(parents=True, exist_ok=True)

    for section in SECTIONS:
        if not section.get("include", True):
            continue

        slug = section["slug"]
        title = section["title"]
        lessons = section.get("lessons", [])

        section_dir = Path(slug)
        section_dir.mkdir(parents=True, exist_ok=True)

        index_path = section_dir / "index.rst"
        write_if_missing(index_path, build_section_index(section))

        if INCLUDE_CSV_TABLES:
            csv_path = csv_dir / f"{slug.replace('-', '_')}_pages.csv"
            write_if_missing(csv_path, build_section_csv(section))

        if SCAFFOLD_LESSONS:
            for lesson in lessons:
                lesson_title = title_from_slug(lesson)
                lesson_path = section_dir / f"{lesson}.md"
                write_if_missing(lesson_path, lesson_body(title, lesson, lesson_title))


if __name__ == "__main__":
    main()
