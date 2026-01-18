# snippets/db/runner.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence

import pandas as pd
from .base import DBConnection


@dataclass
class QueryRunner:
    db: DBConnection

    def execute(self, query: str, params: Optional[Sequence[Any]] = None) -> int:
        self.db.cursor.execute(query, params or [])
        # Commit for statements that modify data
        try:
            self.db.connection.commit()
        except Exception:
            # Some DBs/autocommit settings may not need commit
            pass
        return getattr(self.db.cursor, "rowcount", -1)

    def fetch_df(self, query: str, params: Optional[Sequence[Any]] = None) -> pd.DataFrame:
        self.db.cursor.execute(query, params or [])
        if self.db.cursor.description is None:
            return pd.DataFrame()

        colnames = [desc[0] for desc in self.db.cursor.description]
        rows = self.db.cursor.fetchall()
        return pd.DataFrame(rows, columns=colnames)

    def fetch_scalar(self, query: str, params: Optional[Sequence[Any]] = None, default: Any = None) -> Any:
        self.db.cursor.execute(query, params or [])
        row = self.db.cursor.fetchone()
        if row is None:
            return default
        return row[0]
