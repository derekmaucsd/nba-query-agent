import argparse
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from google import genai


DB_PATH = Path("nba.sqlite")
MODEL_NAME = "gemini-2.5-flash"
ENV_PATH = Path(".env")
MAX_SUBQUERIES = 4
DEFAULT_MAX_RETRIES = 2
SUBQUERY_VALIDATION_ROUNDS = 1
PREVIEW_ROW_LIMIT = 10


@dataclass
class QueryAttempt:
    sql: str
    columns: list[str]
    rows: list[sqlite3.Row]
    error: str | None = None


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


def clean_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else ""
        cleaned = cleaned.replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def is_read_only_sql(sql_query: str) -> bool:
    normalized = sql_query.strip().rstrip(";").strip()
    if not normalized:
        return False
    if ";" in normalized:
        return False
    return normalized.lower().startswith(("select ", "with "))


def generate_sql(
    client: genai.Client,
    user_question: str,
    schema_summary: str,
    evidence: str = "",
    previous_attempts: str = "",
) -> str:
    evidence_block = f"""
Validated subquery evidence:
{evidence}
""" if evidence else ""
    attempts_block = f"""
Previous failed attempts:
{previous_attempts}
""" if previous_attempts else ""

    prompt = f"""
You are writing a SQLite query for the local NBA database.
Return only SQL, no markdown, no explanation.
Only return a single read-only SELECT statement or WITH query.
If the database does not contain the data needed to answer the question, return a
SELECT statement with one text column named answer explaining the limitation.

Database schema:
{schema_summary}

{evidence_block}
{attempts_block}

User question:
{user_question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return clean_sql(response.text or "")


def generate_subquery_plan(
    client: genai.Client,
    user_question: str,
    schema_summary: str,
    max_subqueries: int = MAX_SUBQUERIES,
    previous_evidence: str = "",
    validation_feedback: str = "",
) -> list[dict[str, str]]:
    previous_evidence_block = f"""
Previous subquery evidence:
{previous_evidence}
""" if previous_evidence else ""
    validation_feedback_block = f"""
Validation feedback to address:
{validation_feedback}
""" if validation_feedback else ""

    prompt = f"""
You are helping plan a reliable SQLite answer for a local NBA database.

Break the user's question into up to {max_subqueries} small read-only diagnostic
subqueries. These subqueries should verify:
- which table(s) contain the needed facts,
- the relevant column names and grains,
- sample values or aggregate counts,
- whether the database can actually answer the question.

Return only valid JSON in this shape:
{{
  "subqueries": [
    {{
      "name": "short_snake_case_name",
      "purpose": "what this validates",
      "sql": "single read-only SQLite SELECT/WITH query",
      "expected_signal": "what a useful result should show"
    }}
  ]
}}

Rules:
- Use only tables and columns from the schema below.
- Each SQL value must be one statement and must start with SELECT or WITH.
- Prefer COUNT, GROUP BY, DISTINCT, MIN/MAX, and small LIMIT samples.
- Include LIMIT on non-aggregate sample queries.
- Do not write INSERT, UPDATE, DELETE, CREATE, DROP, PRAGMA, or ATTACH.

Database schema:
{schema_summary}

{previous_evidence_block}
{validation_feedback_block}

User question:
{user_question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    data = clean_json(response.text or "{}")
    subqueries = data.get("subqueries", [])
    if not isinstance(subqueries, list):
        return []
    return [
        item
        for item in subqueries[:max_subqueries]
        if isinstance(item, dict) and isinstance(item.get("sql"), str)
    ]


def validate_subquery_evidence(
    client: genai.Client,
    user_question: str,
    schema_summary: str,
    evidence: str,
) -> dict[str, Any]:
    prompt = f"""
You are validating whether executed SQL subqueries provide enough evidence to
answer a user's NBA database question reliably.

Return only valid JSON in this shape:
{{
  "is_sufficient": true,
  "can_answer": true,
  "reason": "short explanation",
  "missing_checks": ["additional checks needed, if any"]
}}

Set "is_sufficient" to true when the evidence is enough either to answer the
question or to confidently say the database lacks the required data.
Set "can_answer" to false if the schema/evidence shows the requested facts are
not available at the needed grain.

Database schema:
{schema_summary}

Executed subquery evidence:
{evidence}

User question:
{user_question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    data = clean_json(response.text or "{}")
    return data if isinstance(data, dict) else {}


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


def run_subquery_plan(db_path: Path, subqueries: list[dict[str, str]]) -> str:
    evidence_blocks = []
    for idx, subquery in enumerate(subqueries, start=1):
        name = subquery.get("name", f"subquery_{idx}")
        purpose = subquery.get("purpose", "")
        expected_signal = subquery.get("expected_signal", "")
        sql_query = clean_sql(subquery["sql"])
        attempt = execute_query_attempt(db_path, sql_query)

        evidence_blocks.append(
            "\n".join(
                [
                    f"Subquery {idx}: {name}",
                    f"Purpose: {purpose}",
                    f"Expected signal: {expected_signal}",
                    format_attempt(attempt),
                ]
            )
        )
    return "\n\n".join(evidence_blocks)


def collect_validated_evidence(
    client: genai.Client,
    db_path: Path,
    user_question: str,
    schema_summary: str,
    rounds: int = SUBQUERY_VALIDATION_ROUNDS,
) -> str:
    evidence_blocks = []
    validation_feedback = ""

    for _ in range(max(1, rounds)):
        subqueries = generate_subquery_plan(
            client,
            user_question,
            schema_summary,
            previous_evidence="\n\n".join(evidence_blocks),
            validation_feedback=validation_feedback,
        )
        if not subqueries:
            break

        evidence = run_subquery_plan(db_path, subqueries)
        evidence_blocks.append(evidence)
        combined_evidence = "\n\n".join(evidence_blocks)

        validation = validate_subquery_evidence(
            client,
            user_question,
            schema_summary,
            combined_evidence,
        )
        validation_feedback = json.dumps(validation, default=str)
        if validation.get("is_sufficient") is True:
            evidence_blocks.append(f"Subquery validation: {validation_feedback}")
            break

    if validation_feedback and not any(
        block.startswith("Subquery validation:") for block in evidence_blocks
    ):
        evidence_blocks.append(f"Subquery validation: {validation_feedback}")

    return "\n\n".join(evidence_blocks)


def generate_validated_sql(
    client: genai.Client,
    db_path: Path,
    user_question: str,
    schema_summary: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> QueryAttempt:
    try:
        evidence = collect_validated_evidence(client, db_path, user_question, schema_summary)
    except Exception as exc:
        evidence = f"Subquery planning failed: {exc}"
    previous_attempts = []
    attempt = QueryAttempt(sql="", columns=[], rows=[], error="No attempts were run.")

    for _ in range(max(1, max_retries)):
        sql_query = generate_sql(
            client,
            user_question,
            schema_summary,
            evidence=evidence,
            previous_attempts="\n\n".join(previous_attempts),
        )
        attempt = execute_query_attempt(db_path, sql_query)
        if not attempt.error:
            return attempt

        previous_attempts.append(format_attempt(attempt))

    return attempt


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
    parser = argparse.ArgumentParser(description="Run Gemini-to-SQL against nba.sqlite.")
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
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help="Maximum final-query generation attempts after subquery validation.",
    )
    parser.add_argument(
        "--one-shot",
        action="store_true",
        help="Skip subquery planning and retry validation; use the original one-shot flow.",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    client = get_client()
    schema_summary = build_schema_summary(db_path)

    print(f"User question: {args.question}")
    if args.one_shot:
        print("\nGenerating SQL...")
        sql_query = generate_sql(client, args.question, schema_summary)
        print(sql_query)

        print("\nExecuting query...")
        try:
            columns, rows = execute_query(db_path, sql_query)
        except Exception as exc:
            print(f"Database error: {exc}")
            raise SystemExit(1)
    else:
        print("\nPlanning and validating subqueries...")
        attempt = generate_validated_sql(
            client,
            db_path,
            args.question,
            schema_summary,
            max_retries=args.max_retries,
        )
        print("\nFinal SQL:")
        print(attempt.sql)
        if attempt.error:
            print(f"\nDatabase error after retries: {attempt.error}")
            raise SystemExit(1)
        columns = attempt.columns
        rows = attempt.rows

    print("\nQuery result:")
    print_table(columns, rows)


if __name__ == "__main__":
    main()
