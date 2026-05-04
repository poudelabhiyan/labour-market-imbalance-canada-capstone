"""Forecast evaluation metrics for labour market time-series models."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    """Return standard regression metrics for forecast evaluation.

    Parameters
    ----------
    y_true:
        Actual observed values.
    y_pred:
        Predicted values from a model.

    Returns
    -------
    dict
        MAE, RMSE, MAPE, and R-squared.
    """
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)

    mask = ~(np.isnan(actual) | np.isnan(predicted))
    actual = actual[mask]
    predicted = predicted[mask]

    if actual.size == 0:
        raise ValueError("No valid observations available for metric calculation.")

    non_zero_mask = actual != 0
    mape = np.nan
    if non_zero_mask.any():
        mape = float(np.mean(np.abs((actual[non_zero_mask] - predicted[non_zero_mask]) / actual[non_zero_mask])) * 100)

    return {
        "MAE": float(mean_absolute_error(actual, predicted)),
        "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
        "MAPE": mape,
        "R2": float(r2_score(actual, predicted)) if actual.size > 1 else np.nan,
    }


def train_test_summary(
    model_name: str,
    y_train_true,
    y_train_pred,
    y_test_true,
    y_test_pred,
) -> pd.DataFrame:
    """Create a recruiter-friendly train vs test summary table.

    This supports the capstone requirement to compare Train R², Test R²,
    RMSE, and MAE for each model.
    """
    train = regression_metrics(y_train_true, y_train_pred)
    test = regression_metrics(y_test_true, y_test_pred)

    return pd.DataFrame(
        [
            {
                "Model": model_name,
                "Train R2": train["R2"],
                "Test R2": test["R2"],
                "RMSE": test["RMSE"],
                "MAE": test["MAE"],
                "MAPE": test["MAPE"],
            }
        ]
    )


def add_error_columns(
    df: pd.DataFrame,
    actual_col: str,
    forecast_col: str,
) -> pd.DataFrame:
    """Add forecast error columns to a prediction table."""
    result = df.copy()
    result["error"] = result[actual_col] - result[forecast_col]
    result["absolute_error"] = result["error"].abs()
    result["squared_error"] = result["error"] ** 2

    result["absolute_percentage_error"] = np.where(
        result[actual_col] != 0,
        result["absolute_error"] / result[actual_col].abs() * 100,
        np.nan,
    )
    return result
