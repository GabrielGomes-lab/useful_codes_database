# snippets/db/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Protocol


class DBConnector(Protocol):
    def connect(self) -> Any: ...
    def close(self) -> None: ...


@dataclass
class DBConnection:
    """Small wrapper to keep a DB-API connection + cursor together."""
    connection: Any
    cursor: Any

    def close(self) -> None:
        try:
            self.cursor.close()
        finally:
            self.connection.close()
