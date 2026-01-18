# tools/db_exporter/exporters.py
from __future__ import annotations

from pathlib import Path
import pandas as pd


def export_df(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = out_path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(out_path, index=False, encoding="utf-8")
    elif suffix == ".parquet":
        df.to_parquet(out_path, index=False)
    elif suffix == ".xlsx":
        df.to_excel(out_path, index=False)
    else:
        raise ValueError("Output format not supported. Use .csv, .parquet, or .xlsx")
