import argparse
import sqlite3
from pathlib import Path


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def scalar(conn: sqlite3.Connection, query: str, params=()):
    return conn.execute(query, params).fetchone()[0]


def fetch_rows(conn: sqlite3.Connection, query: str, params=(), limit: int = 5):
    cursor = conn.execute(query, params)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchmany(limit)
    return columns, rows


def markdown_table(columns, rows) -> str:
    if not columns:
        return ""

    rendered_rows = []
    for row in rows:
        rendered_rows.append([
            "" if value is None else str(value).replace("\n", " ")[:120]
            for value in row
        ])

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rendered_rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def table_info(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA table_info({quote_ident(table_name)})").fetchall()


def foreign_keys(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA foreign_key_list({quote_ident(table_name)})").fetchall()


def indexes(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA index_list({quote_ident(table_name)})").fetchall()


def analyze_database(db_path: Path, sample_rows: int) -> str:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA query_only = ON")
        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()
        table_names = [row[0] for row in tables]

        lines = [
            "# NBA SQLite EDA",
            "",
            f"Database: `{db_path}`",
            f"Size: {db_path.stat().st_size:,} bytes",
            f"Tables: {len(table_names)}",
            "",
            "## Table Summary",
            "",
            "| table | rows | columns | foreign_keys | indexes |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]

        summaries = []
        for table_name in table_names:
            qname = quote_ident(table_name)
            row_count = scalar(conn, f"SELECT COUNT(*) FROM {qname}")
            columns = table_info(conn, table_name)
            fks = foreign_keys(conn, table_name)
            idxs = indexes(conn, table_name)
            summaries.append((table_name, row_count, columns, fks, idxs))
            lines.append(
                f"| `{table_name}` | {row_count:,} | {len(columns)} | {len(fks)} | {len(idxs)} |"
            )

        lines.extend(["", "## Tables", ""])

        for table_name, row_count, columns, fks, idxs in summaries:
            qname = quote_ident(table_name)
            lines.extend([
                f"### `{table_name}`",
                "",
                f"Rows: {row_count:,}",
                "",
                "| column | type | nullable | primary_key | default |",
                "| --- | --- | --- | --- | --- |",
            ])

            for cid, name, col_type, notnull, default, pk in columns:
                nullable = "no" if notnull else "yes"
                default_value = "" if default is None else str(default)
                lines.append(
                    f"| `{name}` | `{col_type}` | {nullable} | {pk if pk else ''} | {default_value} |"
                )

            if fks:
                lines.extend(["", "Foreign keys:", ""])
                lines.append("| from | to_table | to_column | on_update | on_delete |")
                lines.append("| --- | --- | --- | --- | --- |")
                for fk in fks:
                    lines.append(f"| `{fk[3]}` | `{fk[2]}` | `{fk[4]}` | {fk[5]} | {fk[6]} |")

            if idxs:
                lines.extend(["", "Indexes:", ""])
                lines.append("| name | unique | origin | partial |")
                lines.append("| --- | --- | --- | --- |")
                for idx in idxs:
                    lines.append(f"| `{idx[1]}` | {bool(idx[2])} | {idx[3]} | {bool(idx[4])} |")

            if row_count:
                lines.extend(["", f"Sample rows ({min(sample_rows, row_count)}):", ""])
                col_names = [column[1] for column in columns]
                select_cols = ", ".join(quote_ident(column) for column in col_names)
                sample_columns, sample = fetch_rows(
                    conn,
                    f"SELECT {select_cols} FROM {qname} LIMIT ?",
                    (sample_rows,),
                    sample_rows,
                )
                lines.append(markdown_table(sample_columns, sample))

            lines.append("")

        return "\n".join(lines)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Run quick EDA against nba.sqlite.")
    parser.add_argument("--db", default="nba.sqlite", help="Path to SQLite database.")
    parser.add_argument("--out", default="reports/sqlite_eda.md", help="Markdown report path.")
    parser.add_argument("--sample-rows", type=int, default=3, help="Sample rows per table.")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    report = analyze_database(db_path, args.sample_rows)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
