"""Project configuration for the Labour Market Imbalance Canada capstone project.

The paths are written relative to the repository root so the code can run on
any machine after the repository is cloned.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "1_data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DEFAULT_MODELING_DATASET = PROCESSED_DATA_DIR / "final_dataset_modeling.csv"
DEFAULT_QUALITY_REPORT = PROCESSED_DATA_DIR / "data_quality_report.csv"

DATE_COLUMN = "month"
TARGET_COLUMNS = ["Unemployment", "vacancies"]
DERIVED_RATIO_COLUMN = "theta"

REQUIRED_COLUMNS = [
    "month",
    "Employment",
    "Unemployment",
    "Labour force",
    "Population",
    "vacancies",
    "theta",
]

NUMERIC_COLUMNS = [
    "Employment",
    "Unemployment",
    "Labour force",
    "Population",
    "vacancies",
    "theta",
]
