import argparse
import sqlite3
from pathlib import Path


GRAIN_NOTES = {
    "common_player_info": "One row per player profile (`person_id`).",
    "draft_combine_stats": "One row per player at an NBA Draft Combine season (`season`, `player_id` / player name).",
    "draft_history": "One row per drafted player selection (`season`, `round_number`, `overall_pick`, `person_id`).",
    "game": "One row per game, with home and away team box-score fields on the same row (`game_id`).",
    "game_info": "One row per game with attendance and duration metadata (`game_id`).",
    "game_summary": "One row per game status/summary record (`game_id`).",
    "inactive_players": "One row per inactive player for a game (`game_id`, `player_id`).",
    "line_score": "One row per game line score, with home and away quarter scoring on the same row (`game_id`).",
    "officials": "One row per official assigned to a game (`game_id`, `official_id`).",
    "other_stats": "One row per game with extra home and away team stats on the same row (`game_id`).",
    "play_by_play": "One row per play/event in a game (`game_id`, `eventnum`).",
    "player": "One row per player identity (`id`).",
    "team": "One row per current NBA team (`id`).",
    "team_details": "One row per team details record (`team_id`).",
    "team_history": "One row per team identity era/history segment (`team_id`, `year_founded`).",
    "team_info_common": "Intended grain appears to be one team-season snapshot (`team_id`, `season_year`), but this table is empty in the current database.",
}


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


def escape_markdown_cell(value) -> str:
    return str(value).replace("|", "\\|")


def table_info(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA table_info({quote_ident(table_name)})").fetchall()


def foreign_keys(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA foreign_key_list({quote_ident(table_name)})").fetchall()


def indexes(conn: sqlite3.Connection, table_name: str):
    return conn.execute(f"PRAGMA index_list({quote_ident(table_name)})").fetchall()


def add_data_recency_section(conn: sqlite3.Connection, lines: list[str]) -> None:
    lines.extend([
        "",
        "## Data Recency",
        "",
        "The database is current through the 2022-23 NBA season at the game level. "
        "Game-level tables include the 2023 NBA Finals through June 12, 2023, while "
        "`play_by_play` currently stops at June 9, 2023.",
        "",
        "### Game Coverage",
        "",
        "| season_type | rows | games | min_date | max_date | min_season_id | max_season_id |",
        "| --- | ---: | ---: | --- | --- | --- | --- |",
    ])

    for row in conn.execute(
        """
        SELECT season_type, COUNT(*) rows, COUNT(DISTINCT game_id) games,
               MIN(game_date) min_date, MAX(game_date) max_date,
               MIN(season_id) min_season_id, MAX(season_id) max_season_id
        FROM game
        GROUP BY season_type
        ORDER BY max_date DESC
        """
    ):
        season_type, rows, games, min_date, max_date, min_season_id, max_season_id = row
        lines.append(
            f"| {season_type} | {rows:,} | {games:,} | {min_date} | {max_date} | "
            f"{min_season_id} | {max_season_id} |"
        )

    lines.extend([
        "",
        "### Latest Games",
        "",
    ])
    columns, rows = fetch_rows(
        conn,
        """
        SELECT game_id, game_date, season_id, season_type, matchup_home, wl_home, matchup_away, wl_away
        FROM game
        ORDER BY game_date DESC, game_id DESC
        LIMIT 5
        """,
        limit=5,
    )
    lines.append(markdown_table(columns, rows))

    lines.extend([
        "",
        "### Date Ranges By Table",
        "",
        "| table | date basis | rows | distinct_games | min_date_or_season | max_date_or_season | notes |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ])

    recency_rows = [
        ("game", "game_date", "SELECT COUNT(*), COUNT(DISTINCT game_id), MIN(game_date), MAX(game_date) FROM game", ""),
        ("game_info", "game_date", "SELECT COUNT(*), COUNT(DISTINCT game_id), MIN(game_date), MAX(game_date) FROM game_info", ""),
        ("game_summary", "game_date_est", "SELECT COUNT(*), COUNT(DISTINCT game_id), MIN(game_date_est), MAX(game_date_est) FROM game_summary", ""),
        ("line_score", "game_date_est", "SELECT COUNT(*), COUNT(DISTINCT game_id), MIN(game_date_est), MAX(game_date_est) FROM line_score", ""),
        (
            "play_by_play",
            "joined game.game_date",
            """
            WITH game_dates AS (
                SELECT game_id, MIN(game_date) game_date
                FROM game
                GROUP BY game_id
            )
            SELECT COUNT(*), COUNT(DISTINCT p.game_id), MIN(g.game_date), MAX(g.game_date)
            FROM play_by_play p
            LEFT JOIN game_dates g ON p.game_id = g.game_id
            """,
            "Latest play-by-play is one game date earlier than latest game-level data.",
        ),
        (
            "inactive_players",
            "joined game.game_date",
            """
            WITH game_dates AS (
                SELECT game_id, MIN(game_date) game_date
                FROM game
                GROUP BY game_id
            )
            SELECT COUNT(*), COUNT(DISTINCT i.game_id), MIN(g.game_date), MAX(g.game_date)
            FROM inactive_players i
            LEFT JOIN game_dates g ON i.game_id = g.game_id
            """,
            "",
        ),
        (
            "officials",
            "joined game.game_date",
            """
            WITH game_dates AS (
                SELECT game_id, MIN(game_date) game_date
                FROM game
                GROUP BY game_id
            )
            SELECT COUNT(*), COUNT(DISTINCT o.game_id), MIN(g.game_date), MAX(g.game_date)
            FROM officials o
            LEFT JOIN game_dates g ON o.game_id = g.game_id
            """,
            "",
        ),
        (
            "other_stats",
            "joined game.game_date",
            """
            WITH game_dates AS (
                SELECT game_id, MIN(game_date) game_date
                FROM game
                GROUP BY game_id
            )
            SELECT COUNT(*), COUNT(DISTINCT s.game_id), MIN(g.game_date), MAX(g.game_date)
            FROM other_stats s
            LEFT JOIN game_dates g ON s.game_id = g.game_id
            """,
            "",
        ),
        ("draft_history", "season", "SELECT COUNT(*), 0, MIN(season), MAX(season) FROM draft_history", ""),
        ("draft_combine_stats", "season", "SELECT COUNT(*), 0, MIN(season), MAX(season) FROM draft_combine_stats", ""),
    ]

    for table_name, basis, query, notes in recency_rows:
        rows, distinct_games, min_value, max_value = conn.execute(query).fetchone()
        lines.append(
            f"| `{table_name}` | {basis} | {rows:,} | "
            f"{distinct_games if distinct_games else ''} | {min_value} | {max_value} | {notes} |"
        )

    active_counts = conn.execute(
        "SELECT is_active, COUNT(*) FROM player GROUP BY is_active ORDER BY is_active"
    ).fetchall()
    active_text = ", ".join(f"`is_active={flag}`: {count:,}" for flag, count in active_counts)
    lines.extend([
        "",
        "### Other Recency Signals",
        "",
        f"- `player` active flags: {active_text}.",
    ])

    from_year, max_from_year, min_to_year, max_to_year, min_draft_year, max_draft_year = conn.execute(
        """
        SELECT MIN(from_year), MAX(from_year), MIN(to_year), MAX(to_year),
               MIN(draft_year), MAX(draft_year)
        FROM common_player_info
        WHERE draft_year != 'Undrafted'
        """
    ).fetchone()
    lines.append(
        "- `common_player_info` spans "
        f"`from_year` {from_year:g}-{max_from_year:g}, "
        f"`to_year` {min_to_year:g}-{max_to_year:g}, and drafted-player `draft_year` "
        f"{min_draft_year}-{max_draft_year}."
    )

    duplicate_rows = conn.execute(
        "SELECT COUNT(*) - COUNT(DISTINCT game_id) FROM game"
    ).fetchone()[0]
    lines.append(
        f"- `game` has {duplicate_rows} duplicate `game_id` rows, primarily from both "
        "`All-Star` and `All Star` season type labels for the same All-Star games."
    )


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
            "| table | inferred grain | rows | columns | foreign_keys | indexes |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]

        summaries = []
        for table_name in table_names:
            qname = quote_ident(table_name)
            row_count = scalar(conn, f"SELECT COUNT(*) FROM {qname}")
            columns = table_info(conn, table_name)
            fks = foreign_keys(conn, table_name)
            idxs = indexes(conn, table_name)
            summaries.append((table_name, row_count, columns, fks, idxs))
            grain = escape_markdown_cell(GRAIN_NOTES.get(table_name, "Not inferred."))
            lines.append(
                f"| `{table_name}` | {grain} | {row_count:,} | {len(columns)} | {len(fks)} | {len(idxs)} |"
            )

        add_data_recency_section(conn, lines)

        lines.extend(["", "## Tables", ""])

        for table_name, row_count, columns, fks, idxs in summaries:
            qname = quote_ident(table_name)
            lines.extend([
                f"### `{table_name}`",
                "",
                f"Inferred grain: {GRAIN_NOTES.get(table_name, 'Not inferred.')}",
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
