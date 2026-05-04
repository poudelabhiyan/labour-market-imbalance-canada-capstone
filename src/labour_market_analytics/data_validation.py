"""Data loading and validation helpers for the labour market imbalance project.

The functions in this module are intentionally lightweight and notebook-friendly.
They help keep repeated validation logic outside the analysis notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = {
    "month",
    "Employment",
    "Unemployment",
    "Labour force",
    "Population",
    "vacancies",
    "theta",
}


@dataclass(frozen=True)
class ValidationResult:
    """Simple container for dataset validation results."""

    row_count: int
    column_count: int
    missing_required_columns: list[str]
    duplicate_rows: int
    missing_values: dict[str, int]
    date_min: str | None
    date_max: str | None

    @property
    def passed(self) -> bool:
        """Return True when required columns exist and no duplicate rows are found."""
        return not self.missing_required_columns and self.duplicate_rows == 0


def load_modeling_dataset(path: str | Path) -> pd.DataFrame:
    """Load the final modeling dataset and parse the month column.

    Parameters
    ----------
    path:
        Path to the CSV file. Expected project path:
        ``1_data/processed/final_dataset_modeling.csv``.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset sorted by month.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"], errors="coerce")
        df = df.sort_values("month").reset_index(drop=True)

    return df


def validate_modeling_dataset(
    df: pd.DataFrame,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> ValidationResult:
    """Validate the core modeling dataset.

    The validation checks column presence, duplicate rows, missing values,
    and available date range.
    """
    required = set(required_columns)
    missing_required = sorted(required.difference(df.columns))
    duplicate_rows = int(df.duplicated().sum())
    missing_values = {column: int(value) for column, value in df.isna().sum().items()}

    date_min = None
    date_max = None
    if "month" in df.columns:
        month_series = pd.to_datetime(df["month"], errors="coerce")
        if month_series.notna().any():
            date_min = month_series.min().strftime("%Y-%m-%d")
            date_max = month_series.max().strftime("%Y-%m-%d")

    return ValidationResult(
        row_count=int(df.shape[0]),
        column_count=int(df.shape[1]),
        missing_required_columns=missing_required,
        duplicate_rows=duplicate_rows,
        missing_values=missing_values,
        date_min=date_min,
        date_max=date_max,
    )


def create_validation_table(result: ValidationResult) -> pd.DataFrame:
    """Convert a ValidationResult into a clean reporting table."""
    return pd.DataFrame(
        [
            {"check": "row_count", "value": result.row_count},
            {"check": "column_count", "value": result.column_count},
            {"check": "missing_required_columns", "value": ", ".join(result.missing_required_columns) or "None"},
            {"check": "duplicate_rows", "value": result.duplicate_rows},
            {"check": "date_min", "value": result.date_min},
            {"check": "date_max", "value": result.date_max},
            {"check": "validation_passed", "value": result.passed},
        ]
    )
