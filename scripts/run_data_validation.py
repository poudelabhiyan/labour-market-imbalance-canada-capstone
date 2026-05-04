"""Run validation checks on the final labour market modeling dataset.

Usage from the repository root:
    python scripts/run_data_validation.py
"""

from __future__ import annotations

from pathlib import Path

from labour_market_analytics.data_validation import (
    create_validation_table,
    load_modeling_dataset,
    validate_modeling_dataset,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "1_data" / "processed" / "final_dataset_modeling.csv"
EXPORT_DIR = PROJECT_ROOT / "4_predictive_forecasting" / "exports" / "data_validation"
EXPORT_PATH = EXPORT_DIR / "modeling_dataset_validation_summary.csv"


def main() -> None:
    """Load, validate, and export a validation summary table."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_modeling_dataset(DATA_PATH)
    validation = validate_modeling_dataset(df)
    validation_table = create_validation_table(validation)
    validation_table.to_csv(EXPORT_PATH, index=False)

    print("Validation complete")
    print(f"Rows: {validation.row_count}")
    print(f"Columns: {validation.column_count}")
    print(f"Date range: {validation.date_min} to {validation.date_max}")
    print(f"Duplicate rows: {validation.duplicate_rows}")
    print(f"Missing required columns: {validation.missing_required_columns or 'None'}")
    print(f"Validation passed: {validation.passed}")
    print(f"Exported summary to: {EXPORT_PATH}")


if __name__ == "__main__":
    main()
