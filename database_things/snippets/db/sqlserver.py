# snippets/db/sqlserver.py
from __future__ import annotations

import os
import pyodbc
from dataclasses import dataclass
from typing import Optional

from .base import DBConnection


@dataclass
class SQLServerConnector:
    driver: str
    server: str
    database: str
    username: str
    password: str
    _db: Optional[DBConnection] = None

    @classmethod
    def from_env(cls) -> "SQLServerConnector":
        database = os.getenv("DB_DATABASE")
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")

        if not all([database, username, password]):
            raise ValueError("DB_DATABASE, DB_USERNAME and DB_PASSWORD must be set")

        return cls(
            driver=os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}"),
            server=os.getenv("DB_SERVER", "localhost"),
            database=database,
            username=username,
            password=password,
        )

    def connect(self) -> DBConnection:
        conn = pyodbc.connect(
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
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
