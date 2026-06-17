import argparse
from pathlib import Path

from agent_core import generate_sql, generate_validated_sql_result
from config import DB_PATH, DEFAULT_MAX_RETRIES
from database import build_schema_summary, execute_query
from llm import get_client
from render import print_table


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
        result = generate_validated_sql_result(
            client,
            db_path,
            args.question,
            schema_summary,
            max_retries=args.max_retries,
        )
        if result.evidence:
            print("\nValidation subqueries:")
            print(result.evidence)

        attempt = result.attempt
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
