# snippets/db/postgres.py
from __future__ import annotations

import os
import psycopg2
from dataclasses import dataclass
from typing import Optional

from .base import DBConnection


@dataclass
class PostgresConnector:
    host: str
    port: str
    user: str
    password: str
    dbname: str
    _db: Optional[DBConnection] = None

    @classmethod
    def from_env(cls) -> "PostgresConnector":
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        dbname = os.getenv("DB_NAME")

        if not all([user, password, dbname]):
            raise ValueError("DB_USER, DB_PASSWORD and DB_NAME must be set")

        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=user,
            password=password,
            dbname=dbname,
        )

    def connect(self) -> DBConnection:
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
        )
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
