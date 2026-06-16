import argparse
import os
import sqlite3
from pathlib import Path

from google import genai


DB_PATH = Path("nba.sqlite")
MODEL_NAME = "gemini-2.5-flash"
ENV_PATH = Path(".env")


def load_env_file(env_path: Path = ENV_PATH) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def get_client() -> genai.Client:
    load_env_file()
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running."
        )
    return genai.Client(api_key=api_key)


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


def clean_sql(text: str) -> str:
    sql = text.strip()
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[1] if "\n" in sql else ""
        sql = sql.replace("```", "").strip()
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    return sql


def generate_sql(client: genai.Client, user_question: str, schema_summary: str) -> str:
    prompt = f"""
You are writing a SQLite query for the local NBA database.
Return only SQL, no markdown, no explanation.

Database schema:
{schema_summary}

User question:
{user_question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return clean_sql(response.text or "")


def execute_query(db_path: Path, sql_query: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        return columns, rows
    finally:
        conn.close()


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


def main():
    parser = argparse.ArgumentParser(description="Run a simple Gemini-to-SQL demo against nba.sqlite.")
    parser.add_argument(
        "--question",
        default="How many games were there total in the NBA?",
        help="Natural language question to send to Gemini.",
    )
    parser.add_argument(
        "--db",
        default=str(DB_PATH),
        help="Path to the local SQLite database.",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    client = get_client()
    schema_summary = build_schema_summary(db_path)

    print(f"User question: {args.question}")
    print("\nGenerating SQL...")
    sql_query = generate_sql(client, args.question, schema_summary)
    print(sql_query)

    print("\nExecuting query...")
    try:
        columns, rows = execute_query(db_path, sql_query)
    except Exception as exc:
        print(f"Database error: {exc}")
        raise SystemExit(1)

    print("\nQuery result:")
    print_table(columns, rows)


if __name__ == "__main__":
    main()
