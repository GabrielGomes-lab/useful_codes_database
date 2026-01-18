# snippets/db/sqlite.py
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from .base import DBConnection


@dataclass
class SQLiteConnector:
    path: str
    _db: Optional[DBConnection] = None

    def connect(self) -> DBConnection:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        self._db = DBConnection(conn, cur)
        return self._db

    def close(self) -> None:
        if self._db:
            self._db.close()
            self._db = None

    def __enter__(self) -> DBConnection:
        return self.connect()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
