from dataclasses import dataclass
import sqlite3


@dataclass
class QueryAttempt:
    sql: str
    columns: list[str]
    rows: list[sqlite3.Row]
    error: str | None = None


@dataclass
class ValidatedQueryResult:
    attempt: QueryAttempt
    evidence: str
