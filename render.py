import json
from typing import Any

from config import PREVIEW_ROW_LIMIT
from models import QueryAttempt


def row_preview(columns, rows, limit: int = PREVIEW_ROW_LIMIT) -> list[dict[str, Any]]:
    preview = []
    for row in rows[:limit]:
        preview.append({col: row[col] for col in columns})
    return preview


def format_attempt(attempt: QueryAttempt, include_sql: bool = True) -> str:
    lines = []
    if include_sql:
        lines.append(f"SQL: {attempt.sql}")
    if attempt.error:
        lines.append(f"ERROR: {attempt.error}")
        return "\n".join(lines)

    lines.append(f"Columns: {attempt.columns}")
    lines.append(f"Rows returned: {len(attempt.rows)}")
    lines.append(f"Preview: {json.dumps(row_preview(attempt.columns, attempt.rows), default=str)}")
    return "\n".join(lines)


def print_table(columns, rows):
    if not columns:
        print("(no columns returned)")
        return

    rendered_rows = []
    for row in rows:
        rendered_rows.append([row[col] for col in columns])

    widths = [len(col) for col in columns]
    for row in rendered_rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len("" if value is None else str(value)))

    def render_row(values):
        return " | ".join(
            ("" if value is None else str(value)).ljust(widths[idx])
            for idx, value in enumerate(values)
        )

    print(render_row(columns))
    print(" | ".join("-" * width for width in widths))
    for row in rendered_rows:
        print(render_row(row))
