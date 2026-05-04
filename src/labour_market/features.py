"""Feature engineering helpers for labour-market forecasting."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from labour_market.config import DATE_COLUMN


def add_time_features(df: pd.DataFrame, date_column: str = DATE_COLUMN) -> pd.DataFrame:
    """Add calendar features from the monthly date column."""

    if date_column not in df.columns:
        raise KeyError(f"Date column not found: {date_column}")

    output = df.copy()
    output[date_column] = pd.to_datetime(output[date_column], errors="coerce")

    if output[date_column].isna().any():
        raise ValueError("Some date values could not be parsed.")

    output["year"] = output[date_column].dt.year
    output["month_number"] = output[date_column].dt.month
    output["quarter"] = output[date_column].dt.quarter
    output["time_index"] = range(len(output))

    return output


def add_lag_features(
    df: pd.DataFrame,
    columns: Iterable[str],
    lags: Iterable[int] = (1, 3, 6, 12),
) -> pd.DataFrame:
    """Add lag features for selected columns.

    Parameters
    ----------
    df:
        Input DataFrame sorted by time.
    columns:
        Columns to lag.
    lags:
        Lag periods in months.
    """

    output = df.copy()

    for column in columns:
        if column not in output.columns:
            raise KeyError(f"Column not found for lag feature: {column}")

        for lag in lags:
            output[f"{column}_lag_{lag}"] = output[column].shift(lag)

    return output


def add_rolling_features(
    df: pd.DataFrame,
    columns: Iterable[str],
    windows: Iterable[int] = (3, 6, 12),
) -> pd.DataFrame:
    """Add rolling mean features for selected columns."""

    output = df.copy()

    for column in columns:
        if column not in output.columns:
            raise KeyError(f"Column not found for rolling feature: {column}")

        for window in windows:
            output[f"{column}_rolling_mean_{window}"] = output[column].rolling(window=window).mean()

    return output


def create_supervised_forecasting_frame(
    df: pd.DataFrame,
    target_columns: Iterable[str],
    feature_columns: Iterable[str] | None = None,
    lags: Iterable[int] = (1, 3, 6, 12),
    windows: Iterable[int] = (3, 6, 12),
) -> pd.DataFrame:
    """Create a modeling frame with time, lag, and rolling features.

    This helper is intended for machine-learning benchmark models. Classical
    time-series models such as SARIMAX or VECM may use a different data format.
    """

    output = add_time_features(df)
    output = add_lag_features(output, columns=target_columns, lags=lags)
    output = add_rolling_features(output, columns=target_columns, windows=windows)

    if feature_columns:
        missing_features = [column for column in feature_columns if column not in output.columns]
        if missing_features:
            raise KeyError(f"Feature columns not found: {missing_features}")

    return output.dropna().reset_index(drop=True)
