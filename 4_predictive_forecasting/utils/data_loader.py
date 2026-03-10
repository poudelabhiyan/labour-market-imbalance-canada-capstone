"""
PhD-grade dataset loader for the Labour Market Imbalance Forecasting project.

Responsibilities
----------------
1. Locate project root automatically
2. Load canonical modeling dataset
3. Normalize column naming
4. Validate schema
5. Enforce economic identities
6. Return clean dataframe ready for forecasting
"""

from pathlib import Path
import pandas as pd
import numpy as np


# -------------------------------------------------------
# Resolve project root
# -------------------------------------------------------

def _get_project_root():
    """
    Assumes this file lives in:

    project_root/
        4_predictive_forecasting/
            utils/
                data_loader.py
    """
    return Path(__file__).resolve().parents[2]


# -------------------------------------------------------
# Canonical schema
# -------------------------------------------------------

REQUIRED_COLUMNS = [
    "month",
    "employment",
    "unemployment",
    "labour_force",
    "population",
    "vacancies",
    "theta"
]


# -------------------------------------------------------
# Main loader
# -------------------------------------------------------

def load_dataset(verbose=True):

    project_root = _get_project_root()

    data_path = (
        project_root /
        "1_data" /
        "processed" /
        "final_dataset_modeling.csv"
    )

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at:\n{data_path}"
        )

    # ---------------------------------------------------
    # Load dataset
    # ---------------------------------------------------

    df = pd.read_csv(data_path)

    # ---------------------------------------------------
    # Normalize column names
    # ---------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ---------------------------------------------------
    # Validate schema
    # ---------------------------------------------------

    missing_cols = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}"
        )

    # ---------------------------------------------------
    # Convert month to datetime
    # ---------------------------------------------------

    df["month"] = pd.to_datetime(df["month"])

    # ---------------------------------------------------
    # Sort chronologically
    # ---------------------------------------------------

    df = df.sort_values("month")

    # ---------------------------------------------------
    # Check duplicate months
    # ---------------------------------------------------

    if df["month"].duplicated().any():
        raise ValueError("Duplicate months detected in dataset")

    # ---------------------------------------------------
    # Ensure numeric columns
    # ---------------------------------------------------

    numeric_cols = [
        "employment",
        "unemployment",
        "labour_force",
        "population",
        "vacancies",
        "theta"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")

    # ---------------------------------------------------
    # Enforce economic identities
    # ---------------------------------------------------

    # Labour force identity
    calculated_lf = df["employment"] + df["unemployment"]

    lf_error = np.abs(df["labour_force"] - calculated_lf)

    if lf_error.mean() > 1e-6:
        print(
            "Warning: labour_force column inconsistent with "
            "employment + unemployment. Recomputing labour_force."
        )
        df["labour_force"] = calculated_lf

    # Theta identity
    calculated_theta = df["vacancies"] / df["unemployment"]

    theta_error = np.abs(df["theta"] - calculated_theta)

    if theta_error.mean() > 1e-6:
        print(
            "Warning: theta inconsistent with vacancies/unemployment. "
            "Recomputing theta."
        )
        df["theta"] = calculated_theta

    # ---------------------------------------------------
    # Set month as index
    # ---------------------------------------------------

    df = df.set_index("month")

    # ---------------------------------------------------
    # Verbose summary
    # ---------------------------------------------------

    if verbose:

        print("\nDataset loaded successfully")
        print("--------------------------------")

        print("Rows:", len(df))
        print("Period:", df.index.min(), "→", df.index.max())

        print("\nColumns:")
        print(list(df.columns))

        print("\nMissing values:")
        print(df.isna().sum())

        print("\nSummary statistics:")
        print(df.describe().round(2))

    return df


# -------------------------------------------------------
# Script entry point for testing
# -------------------------------------------------------

if __name__ == "__main__":

    print("\nRunning data loader test...\n")

    df = load_dataset(verbose=True)

    print("\nFirst rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)