import sqlite3
from pathlib import Path

from models import QueryAttempt
from sql_utils import is_read_only_sql


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def build_schema_summary(db_path: Path) -> str:
    conn = sqlite3.connect(db_path)
    try:
        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        lines = []
        for (table_name,) in tables:
            columns = conn.execute(
                f"PRAGMA table_info({quote_ident(table_name)})"
            ).fetchall()
            col_text = ", ".join(f"{col[1]} ({col[2]})" for col in columns)
            row_count = conn.execute(
                f"SELECT COUNT(*) FROM {quote_ident(table_name)}"
            ).fetchone()[0]
            lines.append(f"- {table_name} [{row_count} rows]: {col_text}")
        return "\n".join(lines)
    finally:
        conn.close()


def execute_query(db_path: Path, sql_query: str):
    if not is_read_only_sql(sql_query):
        raise ValueError("Generated SQL must be a single read-only SELECT/WITH statement.")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        return columns, rows
    finally:
        conn.close()


def execute_query_attempt(db_path: Path, sql_query: str) -> QueryAttempt:
    try:
        columns, rows = execute_query(db_path, sql_query)
        return QueryAttempt(sql=sql_query, columns=columns, rows=rows)
    except Exception as exc:
        return QueryAttempt(sql=sql_query, columns=[], rows=[], error=str(exc))
