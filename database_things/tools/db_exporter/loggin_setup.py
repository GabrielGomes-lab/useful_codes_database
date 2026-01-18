# tools/db_exporter/logging_setup.py
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger() -> logging.Logger:
    logger = logging.getLogger("db_exporter")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    fh = RotatingFileHandler(log_dir / "db_exporter.log", maxBytes=1_000_000, backupCount=3)
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
