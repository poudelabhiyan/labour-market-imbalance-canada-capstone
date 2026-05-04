"""Data quality utilities for the labour market modeling dataset."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from labour_market.config import DATE_COLUMN, NUMERIC_COLUMNS, REQUIRED_COLUMNS


@dataclass(frozen=True)
class QualityCheckResult:
    """Single data quality check result."""

    check_name: str
    status: str
    details: str


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset and return a pandas DataFrame.

    Parameters
    ----------
    path:
        Path to the CSV file.

    Raises
    ------
    FileNotFoundError
        If the dataset path does not exist.
    ValueError
        If the loaded dataset is empty.
    """

    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)
    if df.empty:
        raise ValueError(f"Dataset is empty: {dataset_path}")

    return df


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> QualityCheckResult:
    """Check whether all required modeling columns exist."""

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        return QualityCheckResult(
            check_name="required_columns",
            status="FAIL",
            details=f"Missing columns: {missing_columns}",
        )

    return QualityCheckResult(
        check_name="required_columns",
        status="PASS",
        details="All required columns are present.",
    )


def summarize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for each column."""

    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)

    return pd.DataFrame(
        {
            "column": missing_count.index,
            "missing_count": missing_count.values,
            "missing_pct": missing_pct.values,
        }
    ).sort_values("missing_pct", ascending=False)


def check_duplicate_rows(df: pd.DataFrame) -> QualityCheckResult:
    """Check whether the dataset contains duplicate rows."""

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        return QualityCheckResult(
            check_name="duplicate_rows",
            status="WARN",
            details=f"Found {duplicate_count} duplicate rows.",
        )

    return QualityCheckResult(
        check_name="duplicate_rows",
        status="PASS",
        details="No duplicate rows found.",
    )


def prepare_month_column(df: pd.DataFrame, date_column: str = DATE_COLUMN) -> pd.DataFrame:
    """Parse and sort the monthly date column."""

    if date_column not in df.columns:
        raise KeyError(f"Date column not found: {date_column}")

    output = df.copy()
    output[date_column] = pd.to_datetime(output[date_column], errors="coerce")
    output = output.sort_values(date_column).reset_index(drop=True)

    return output


def check_monthly_continuity(df: pd.DataFrame, date_column: str = DATE_COLUMN) -> QualityCheckResult:
    """Check whether monthly observations are continuous.

    This check is useful for time-series modeling. If a known period has been
    intentionally removed, the warning should be documented in the notebook.
    """

    prepared = prepare_month_column(df, date_column=date_column)

    if prepared[date_column].isna().any():
        bad_count = int(prepared[date_column].isna().sum())
        return QualityCheckResult(
            check_name="monthly_continuity",
            status="FAIL",
            details=f"Date parsing failed for {bad_count} rows.",
        )

    min_month = prepared[date_column].min()
    max_month = prepared[date_column].max()
    expected_months = pd.date_range(min_month, max_month, freq="MS")
    actual_months = pd.DatetimeIndex(prepared[date_column].dt.to_period("M").dt.to_timestamp())
    missing_months = sorted(set(expected_months) - set(actual_months))

    if missing_months:
        missing_text = [month.strftime("%Y-%m") for month in missing_months]
        return QualityCheckResult(
            check_name="monthly_continuity",
            status="WARN",
            details=f"Missing monthly periods: {missing_text}",
        )

    return QualityCheckResult(
        check_name="monthly_continuity",
        status="PASS",
        details="Monthly date sequence is continuous.",
    )


def check_numeric_columns(
    df: pd.DataFrame,
    numeric_columns: Iterable[str] = NUMERIC_COLUMNS,
) -> pd.DataFrame:
    """Return basic numeric quality statistics for project columns."""

    records: list[dict[str, object]] = []

    for column in numeric_columns:
        if column not in df.columns:
            records.append(
                {
                    "column": column,
                    "exists": False,
                    "non_null_count": np.nan,
                    "min": np.nan,
                    "max": np.nan,
                    "mean": np.nan,
                    "negative_count": np.nan,
                }
            )
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        records.append(
            {
                "column": column,
                "exists": True,
                "non_null_count": int(values.notna().sum()),
                "min": values.min(),
                "max": values.max(),
                "mean": values.mean(),
                "negative_count": int((values < 0).sum()),
            }
        )

    return pd.DataFrame(records)


def validate_theta(
    df: pd.DataFrame,
    unemployment_col: str = "Unemployment",
    vacancy_col: str = "vacancies",
    theta_col: str = "theta",
    tolerance: float = 0.001,
) -> QualityCheckResult:
    """Validate theta as vacancies divided by unemployment.

    Rows with zero unemployment are excluded from the division check to avoid
    invalid division.
    """

    required = [unemployment_col, vacancy_col, theta_col]
    missing = [column for column in required if column not in df.columns]
    if missing:
        return QualityCheckResult(
            check_name="theta_validation",
            status="FAIL",
            details=f"Missing columns for theta validation: {missing}",
        )

    unemployment = pd.to_numeric(df[unemployment_col], errors="coerce")
    vacancies = pd.to_numeric(df[vacancy_col], errors="coerce")
    theta = pd.to_numeric(df[theta_col], errors="coerce")

    valid_mask = unemployment.notna() & vacancies.notna() & theta.notna() & (unemployment != 0)
    if valid_mask.sum() == 0:
        return QualityCheckResult(
            check_name="theta_validation",
            status="FAIL",
            details="No valid rows available for theta validation.",
        )

    recalculated_theta = vacancies[valid_mask] / unemployment[valid_mask]
    max_difference = float((recalculated_theta - theta[valid_mask]).abs().max())

    if max_difference > tolerance:
        return QualityCheckResult(
            check_name="theta_validation",
            status="WARN",
            details=f"Max theta difference is {max_difference:.6f}, above tolerance {tolerance}.",
        )

    return QualityCheckResult(
        check_name="theta_validation",
        status="PASS",
        details=f"Theta values match vacancy/unemployment ratio within tolerance {tolerance}.",
    )


def run_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    """Run project-level quality checks and return a summary table."""

    checks = [
        validate_required_columns(df),
        check_duplicate_rows(df),
        check_monthly_continuity(df),
        validate_theta(df),
    ]

    return pd.DataFrame([check.__dict__ for check in checks])
