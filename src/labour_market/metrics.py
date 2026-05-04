"""Forecast evaluation metrics for the labour-market forecasting phase."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def root_mean_squared_error(y_true, y_pred) -> float:
    """Calculate root mean squared error."""

    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mean_absolute_percentage_error(y_true, y_pred) -> float:
    """Calculate MAPE while safely ignoring zero actual values."""

    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)

    non_zero_mask = actual != 0
    if non_zero_mask.sum() == 0:
        return float("nan")

    return float(np.mean(np.abs((actual[non_zero_mask] - predicted[non_zero_mask]) / actual[non_zero_mask])) * 100)


def evaluate_forecast(y_true, y_pred) -> dict[str, float]:
    """Return standard forecasting metrics for one model output."""

    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": root_mean_squared_error(y_true, y_pred),
        "MAPE": mean_absolute_percentage_error(y_true, y_pred),
        "R2": float(r2_score(y_true, y_pred)),
    }


def build_model_comparison_table(results: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Convert nested model results into a clean comparison table.

    Example
    -------
    results = {
        "SARIMAX_Unemployment": {"MAE": 10.2, "RMSE": 13.4, "MAPE": 4.1, "R2": 0.88},
        "SARIMAX_vacancies": {"MAE": 8.2, "RMSE": 11.1, "MAPE": 3.9, "R2": 0.91},
    }
    """

    table = pd.DataFrame.from_dict(results, orient="index").reset_index()
    table = table.rename(columns={"index": "model"})

    preferred_order = ["model", "MAE", "RMSE", "MAPE", "R2"]
    available_columns = [column for column in preferred_order if column in table.columns]
    remaining_columns = [column for column in table.columns if column not in available_columns]

    return table[available_columns + remaining_columns]


def train_test_performance_summary(
    model_name: str,
    y_train_true,
    y_train_pred,
    y_test_true,
    y_test_pred,
) -> dict[str, float | str]:
    """Create the train-vs-test summary required for the predictive phase."""

    return {
        "Model": model_name,
        "Train R2": float(r2_score(y_train_true, y_train_pred)),
        "Test R2": float(r2_score(y_test_true, y_test_pred)),
        "RMSE": root_mean_squared_error(y_test_true, y_test_pred),
        "MAE": float(mean_absolute_error(y_test_true, y_test_pred)),
    }
