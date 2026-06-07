#!/usr/bin/env python3
"""Summarize recent Codex session token usage.

This script is intentionally standard-library only so workshop participants can
run it from a project checkout without installing packages.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TOKEN_COLUMNS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a recent Codex usage summary from ~/.codex."
    )
    parser.add_argument(
        "--codex-dir",
        default="~/.codex",
        help="Codex home directory. Default: ~/.codex",
    )
    parser.add_argument(
        "--days",
        type=float,
        default=2,
        help="Number of recent days to include. Default: 2",
    )
    parser.add_argument(
        "--out",
        default="codex_usage_summary.md",
        help="Markdown report path. Default: codex_usage_summary.md",
    )
    parser.add_argument(
        "--csv",
        default="codex_usage_sessions.csv",
        help="Per-session CSV path. Default: codex_usage_sessions.csv",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top sessions to show. Default: 10",
    )
    return parser.parse_args()


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def from_unix(value: float | int | None) -> dt.datetime | None:
    if value is None:
        return None
    try:
        raw = float(value)
        if raw > 10_000_000_000:
            raw = raw / 1000
        return dt.datetime.fromtimestamp(raw, tz=dt.timezone.utc)
    except (OSError, OverflowError, TypeError, ValueError):
        return None


def fmt_int(value: int | float | None) -> str:
    if value is None:
        return ""
    return f"{int(value):,}"


def fmt_dt(value: dt.datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone().strftime("%Y-%m-%d %H:%M")


def connect_usage_db(codex_dir: Path) -> sqlite3.Connection:
    db_path = codex_dir / "state_5.sqlite"
    if not db_path.exists():
        raise SystemExit(f"Could not find Codex usage database: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}


def find_usage_table(conn: sqlite3.Connection) -> str:
    tables = [
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        )
    ]
    for table in tables:
        cols = table_columns(conn, table)
        if {"session_id", "total_tokens"}.issubset(cols):
            return table
    raise SystemExit("Could not find a usage table with session_id and total_tokens.")


def has_thread_usage(conn: sqlite3.Connection) -> bool:
    try:
        cols = table_columns(conn, "threads")
    except sqlite3.OperationalError:
        return False
    return {"id", "tokens_used"}.issubset(cols)


def read_thread_sessions(
    conn: sqlite3.Connection, since: dt.datetime
) -> dict[str, dict[str, Any]]:
    cols = table_columns(conn, "threads")
    wanted = [
        c
        for c in (
            "id",
            "title",
            "source",
            "thread_source",
            "model",
            "model_provider",
            "cwd",
            "created_at",
            "updated_at",
            "created_at_ms",
            "updated_at_ms",
            "tokens_used",
            "rollout_path",
            "first_user_message",
            "preview",
        )
        if c in cols
    ]
    sessions: dict[str, dict[str, Any]] = {}
    for row in conn.execute(f"SELECT {', '.join(wanted)} FROM threads"):
        item = dict(row)
        created = from_unix(item.get("created_at_ms") or item.get("created_at"))
        updated = from_unix(item.get("updated_at_ms") or item.get("updated_at"))
        if updated is not None and updated < since:
            continue

        session_id = str(item["id"])
        total = int(item.get("tokens_used") or 0)
        sessions[session_id] = {
            "session_id": session_id,
            "turns": 0,
            "first_seen": created,
            "last_seen": updated,
            "input_tokens": 0,
            "cached_input_tokens": 0,
            "output_tokens": 0,
            "reasoning_output_tokens": 0,
            "total_tokens": total,
            "title": item.get("title") or item.get("first_user_message") or item.get("preview"),
            "source": item.get("source") or item.get("thread_source"),
            "model": item.get("model") or item.get("model_provider"),
            "cwd": item.get("cwd"),
            "jsonl_path": item.get("rollout_path"),
        }
    return sessions


def find_sessions_table(conn: sqlite3.Connection) -> str | None:
    for name in ("sessions", "conversation_sessions"):
        try:
            cols = table_columns(conn, name)
        except sqlite3.OperationalError:
            continue
        if "id" in cols or "session_id" in cols:
            return name
    return None


def read_usage_rows(
    conn: sqlite3.Connection, usage_table: str, since: dt.datetime
) -> list[dict[str, Any]]:
    cols = table_columns(conn, usage_table)
    created_col = next(
        (c for c in ("created_at", "timestamp", "ts", "time") if c in cols), None
    )

    select_cols = ["session_id"] + [c for c in TOKEN_COLUMNS if c in cols]
    if created_col:
        select_cols.append(created_col)

    rows = []
    for row in conn.execute(f"SELECT {', '.join(select_cols)} FROM {usage_table}"):
        item = dict(row)
        created = from_unix(item.get(created_col)) if created_col else None
        if created is not None and created < since:
            continue
        item["_created"] = created
        rows.append(item)
    return rows


def read_session_metadata(conn: sqlite3.Connection) -> dict[str, dict[str, Any]]:
    table = find_sessions_table(conn)
    if table is None:
        return {}

    cols = table_columns(conn, table)
    id_col = "id" if "id" in cols else "session_id"
    wanted = [
        id_col,
        *[
            c
            for c in (
                "title",
                "source",
                "model",
                "created_at",
                "updated_at",
                "cwd",
                "current_dir",
            )
            if c in cols
        ],
    ]
    meta: dict[str, dict[str, Any]] = {}
    for row in conn.execute(f"SELECT {', '.join(wanted)} FROM {table}"):
        item = dict(row)
        session_id = str(item.pop(id_col))
        meta[session_id] = item
    return meta


def aggregate_usage(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    sessions: dict[str, dict[str, Any]] = {}
    for row in rows:
        session_id = str(row["session_id"])
        item = sessions.setdefault(
            session_id,
            {
                "session_id": session_id,
                "turns": 0,
                "first_seen": None,
                "last_seen": None,
                **{col: 0 for col in TOKEN_COLUMNS},
            },
        )
        item["turns"] += 1
        created = row.get("_created")
        if created is not None:
            if item["first_seen"] is None or created < item["first_seen"]:
                item["first_seen"] = created
            if item["last_seen"] is None or created > item["last_seen"]:
                item["last_seen"] = created
        for col in TOKEN_COLUMNS:
            item[col] += int(row.get(col) or 0)
    return sessions


def session_files(codex_dir: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    sessions_dir = codex_dir / "sessions"
    if not sessions_dir.exists():
        return files
    for path in sessions_dir.rglob("*.jsonl"):
        files[path.stem] = path
        match = re.search(
            r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
            path.stem,
        )
        if match:
            files[match.group(1)] = path
    return files


def inspect_jsonl(path: Path, max_lines: int = 20000) -> dict[str, Any]:
    counts = Counter()
    previews: list[str] = []
    first_text: str | None = None
    last_text: str | None = None

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line_number, line in enumerate(fh, start=1):
            if line_number > max_lines:
                counts["truncated"] += 1
                break
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                counts["bad_json"] += 1
                continue

            item_type = str(item.get("type") or item.get("event") or "unknown")
            counts[item_type] += 1

            payload = item.get("payload") if isinstance(item, dict) else None
            payload_type = None
            if isinstance(payload, dict):
                payload_type = payload.get("type")
                if payload_type:
                    counts[str(payload_type)] += 1
                role = payload.get("role")
                if role:
                    counts[f"role:{role}"] += 1

            text = None
            if isinstance(payload, dict) and payload_type in {"user_message", "agent_message"}:
                text = payload.get("message")
            elif isinstance(payload, dict) and payload.get("role") in {"user", "assistant"}:
                text = extract_text(payload.get("content"))
            elif item_type not in {"session_meta", "turn_context"}:
                text = extract_text(item)
            if text:
                text = text.strip()
            if text and is_infrastructure_text(text):
                text = None
            if text:
                if first_text is None:
                    first_text = text
                last_text = text
                if len(previews) < 3:
                    previews.append(text[:180].replace("\n", " "))

            name = extract_tool_name(item)
            if name:
                counts[f"tool:{name}"] += 1

    return {
        "event_counts": dict(counts),
        "first_text": first_text,
        "last_text": last_text,
        "previews": previews,
    }


def extract_text(item: Any) -> str | None:
    if isinstance(item, str):
        return item
    if isinstance(item, list):
        parts = [extract_text(part) for part in item]
        return "\n".join(part for part in parts if part) or None
    if not isinstance(item, dict):
        return None

    for key in ("text", "content", "message", "input"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (dict, list)):
            nested = extract_text(value)
            if nested:
                return nested

    payload = item.get("payload") or item.get("data")
    if isinstance(payload, (dict, list)):
        return extract_text(payload)
    return None


def is_infrastructure_text(text: str) -> bool:
    prefixes = (
        "<permissions instructions>",
        "<collaboration_mode>",
        "<apps_instructions>",
        "<skills_instructions>",
        "<plugins_instructions>",
        "<environment_context>",
        "# AGENTS.md instructions",
    )
    return text.startswith(prefixes)


def extract_tool_name(item: dict[str, Any]) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in ("name", "tool_name", "callable", "recipient"):
        value = item.get(key)
        if isinstance(value, str) and value:
            if any(word in value.lower() for word in ("exec", "mcp", "tool", "read", "write")):
                return value
    payload = item.get("payload") or item.get("data")
    if isinstance(payload, dict):
        return extract_tool_name(payload)
    return None


def classify_session(session: dict[str, Any]) -> str:
    title = str(session.get("title") or "").lower()
    source = str(session.get("source") or "").lower()
    path = str(session.get("jsonl_path") or "").lower()

    if "subagent" in title or "subagent" in source:
        return "subagent"
    if "mcp" in title or "mcp" in source or "mcp" in path:
        return "mcp-related"
    if "jupyter" in title or "jupyter" in source or ".ipynb" in title:
        return "jupyter-related"
    if "@codex" in title or "chat" in title:
        return "jupyter-related"
    if "cli" in source or "terminal" in title:
        return "terminal-codex"
    return "other-or-unknown"


def merge_metadata(
    sessions: dict[str, dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
    files: dict[str, Path],
    inspect_top: int,
) -> list[dict[str, Any]]:
    items = list(sessions.values())
    for item in items:
        if item["session_id"] in metadata:
            item.update(metadata[item["session_id"]])
        if item.get("created_at") and item["first_seen"] is None:
            item["first_seen"] = from_unix(item["created_at"])
        if item.get("updated_at") and item["last_seen"] is None:
            item["last_seen"] = from_unix(item["updated_at"])
        path = files.get(item["session_id"])
        if path:
            item["jsonl_path"] = str(path)

    items.sort(key=lambda row: row.get("total_tokens", 0), reverse=True)

    for item in items[:inspect_top]:
        path_text = item.get("jsonl_path")
        if path_text:
            try:
                item["jsonl"] = inspect_jsonl(Path(path_text))
                if not item.get("turns"):
                    counts = item["jsonl"].get("event_counts") or {}
                    item["turns"] = (
                        counts.get("user_message", 0)
                        or counts.get("role:user", 0)
                        or counts.get("message", 0)
                    )
            except OSError as exc:
                item["jsonl_error"] = str(exc)
        item["bucket"] = classify_session(item)

    for item in items[inspect_top:]:
        item["bucket"] = classify_session(item)

    return items


def write_csv(path: Path, sessions: list[dict[str, Any]]) -> None:
    fields = [
        "session_id",
        "bucket",
        "title",
        "source",
        "turns",
        "first_seen",
        "last_seen",
        *TOKEN_COLUMNS,
        "jsonl_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for item in sessions:
            row = {field: item.get(field, "") for field in fields}
            row["first_seen"] = fmt_dt(item.get("first_seen"))
            row["last_seen"] = fmt_dt(item.get("last_seen"))
            writer.writerow(row)


def write_report(
    path: Path,
    sessions: list[dict[str, Any]],
    codex_dir: Path,
    since: dt.datetime,
    csv_path: Path,
    top: int,
) -> None:
    totals = {col: sum(int(item.get(col) or 0) for item in sessions) for col in TOKEN_COLUMNS}
    by_bucket: dict[str, int] = defaultdict(int)
    by_bucket_sessions: Counter[str] = Counter()
    for item in sessions:
        bucket = str(item.get("bucket") or "other-or-unknown")
        by_bucket[bucket] += int(item.get("total_tokens") or 0)
        by_bucket_sessions[bucket] += 1

    lines = [
        "# Codex Usage Summary",
        "",
        f"- Codex directory: `{codex_dir}`",
        f"- Window starts: `{fmt_dt(since)}`",
        f"- Sessions included: `{len(sessions)}`",
        f"- CSV detail: `{csv_path}`",
        "",
        "## Token Totals",
        "",
        "| Metric | Tokens |",
        "|---|---:|",
    ]
    for col in TOKEN_COLUMNS:
        lines.append(f"| {col} | {fmt_int(totals[col])} |")
    if totals["total_tokens"] and not any(totals[col] for col in TOKEN_COLUMNS[:-1]):
        lines.extend(
            [
                "",
                "This Codex database records total tokens per session, but not the input/output token breakdown. The zero values above mean the detailed breakdown was unavailable.",
            ]
        )

    lines.extend(
        [
            "",
            "## Where Tokens Went",
            "",
            "| Bucket | Sessions | Total tokens | Share |",
            "|---|---:|---:|---:|",
        ]
    )
    grand_total = totals["total_tokens"] or 1
    for bucket, value in sorted(by_bucket.items(), key=lambda pair: pair[1], reverse=True):
        share = value / grand_total
        lines.append(
            f"| {bucket} | {by_bucket_sessions[bucket]} | {fmt_int(value)} | {share:.1%} |"
        )

    lines.extend(
        [
            "",
            "## Top Sessions",
            "",
            "| Rank | Tokens | Turns | Bucket | Started | Title |",
            "|---:|---:|---:|---|---|---|",
        ]
    )
    for rank, item in enumerate(sessions[:top], start=1):
        title = str(item.get("title") or item.get("session_id") or "").replace("|", "\\|")
        lines.append(
            f"| {rank} | {fmt_int(item.get('total_tokens'))} | {item.get('turns', '')} | "
            f"{item.get('bucket', '')} | {fmt_dt(item.get('first_seen'))} | {title[:90]} |"
        )

    lines.extend(
        [
            "",
            "## What To Look For",
            "",
            "- Very large sessions usually contain accumulated conversation history, large tool outputs, notebook outputs, or repeated file inspection.",
            "- Buckets are heuristics based on session title, source, and path. Open the CSV for exact session ids and titles.",
            "- A short prompt can still be expensive when it is sent near the end of a long session.",
            "- If the same data profile appears in many sessions, write the verified facts into `data/README.md` or the notebook.",
            "- If a session has many tool calls but few durable file changes, consider using a fresh session with a narrower prompt.",
            "",
            "## Inspecting The Biggest Sessions",
            "",
        ]
    )

    for item in sessions[:top]:
        lines.append(f"### {fmt_int(item.get('total_tokens'))} tokens: {item.get('title') or item['session_id']}")
        lines.append("")
        lines.append(f"- Session id: `{item['session_id']}`")
        lines.append(f"- Bucket: `{item.get('bucket', '')}`")
        lines.append(f"- Turns: `{item.get('turns', '')}`")
        if item.get("jsonl_path"):
            lines.append(f"- JSONL: `{item['jsonl_path']}`")
        jsonl = item.get("jsonl") or {}
        event_counts = jsonl.get("event_counts") or {}
        tool_counts = {
            key.removeprefix("tool:"): value
            for key, value in event_counts.items()
            if key.startswith("tool:")
        }
        if tool_counts:
            common = ", ".join(
                f"{name} ({count})" for name, count in Counter(tool_counts).most_common(5)
            )
            lines.append(f"- Common tools/events: {common}")
        previews = jsonl.get("previews") or []
        if previews:
            lines.append("- Text preview:")
            for preview in previews:
                lines.append(f"  - {preview}")
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    codex_dir = Path(os.path.expanduser(args.codex_dir)).resolve()
    since = now_utc() - dt.timedelta(days=args.days)

    conn = connect_usage_db(codex_dir)
    if has_thread_usage(conn):
        sessions = read_thread_sessions(conn, since)
        metadata = {}
    else:
        usage_table = find_usage_table(conn)
        usage_rows = read_usage_rows(conn, usage_table, since)
        sessions = aggregate_usage(usage_rows)
        metadata = read_session_metadata(conn)
    files = session_files(codex_dir)
    merged = merge_metadata(sessions, metadata, files, inspect_top=max(args.top, 20))

    out_path = Path(args.out).resolve()
    csv_path = Path(args.csv).resolve()
    write_csv(csv_path, merged)
    write_report(out_path, merged, codex_dir, since, csv_path, args.top)

    total = sum(int(item.get("total_tokens") or 0) for item in merged)
    print(f"Wrote {out_path}")
    print(f"Wrote {csv_path}")
    print(f"Included {len(merged)} sessions and {fmt_int(total)} total tokens.")


if __name__ == "__main__":
    main()
