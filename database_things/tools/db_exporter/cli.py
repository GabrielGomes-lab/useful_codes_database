# tools/db_exporter/cli.py
from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from .db_factory import make_runner
from .exporters import export_df
from .logging_setup import get_logger

log = get_logger()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export DB query results to CSV/Parquet/Excel.")
    p.add_argument("--db", choices=["postgres", "sqlserver", "sqlite"], required=True)
    p.add_argument("--query-file", required=True, help="Path to .sql file")
    p.add_argument("--out", required=True, help="Output path (.csv | .parquet | .xlsx)")
    p.add_argument("--params", nargs="*", default=None, help="Optional query params (strings).")
    p.add_argument("--sqlite-path", default=None, help="Required when --db sqlite")
    return p.parse_args()


def main() -> int:
    load_dotenv()  # reads .env
    args = parse_args()

    query_path = Path(args.query_file)
    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_path}")

    query = query_path.read_text(encoding="utf-8")
    out_path = Path(args.out)

    log.info("Starting export: db=%s query_file=%s out=%s", args.db, args.query_file, args.out)

    runner_ctx = make_runner(db_kind=args.db, sqlite_path=args.sqlite_path)

    with runner_ctx as runner:
        df = runner.fetch_df(query, params=args.params)

    export_df(df, out_path)
    log.info("Export finished: rows=%s cols=%s file=%s", len(df), len(df.columns), out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
