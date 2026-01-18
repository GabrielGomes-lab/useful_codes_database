# tools/db_exporter/db_factory.py
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Optional

from database_things.snippets.postgres import PostgresConnector
from database_things.snippets.sqlserver import SQLServerConnector
from database_things.snippets.sqllite import SQLiteConnector
from database_things.snippets.runner import QueryRunner


@contextmanager
def make_runner(db_kind: str, sqlite_path: Optional[str] = None) -> Iterator[QueryRunner]:
    if db_kind == "postgres":
        connector = PostgresConnector.from_env()
    elif db_kind == "sqlserver":
        connector = SQLServerConnector.from_env()
    elif db_kind == "sqlite":
        if not sqlite_path:
            raise ValueError("--sqlite-path is required when --db sqlite")
        connector = SQLiteConnector(sqlite_path)
    else:
        raise ValueError(f"Unsupported db kind: {db_kind}")

    with connector as db:
        yield QueryRunner(db)
