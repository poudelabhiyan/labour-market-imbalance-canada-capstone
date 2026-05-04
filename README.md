# AI-Driven Labour Market Imbalance Analysis — Canada

**Capstone project:** Master of Data Analytics, University of Niagara Falls Canada  
**Focus:** Labour market imbalance, unemployment, job vacancies, forecasting, and scenario-based workforce planning  
**Country:** Canada  
**Period covered:** 2015–2024 historical analysis with 2026 forecasting outputs in the current repository  
**Core tools:** Python, pandas, statsmodels, scikit-learn, Jupyter Notebook, time-series forecasting, diagnostic analytics

---

## 1. Project Overview

This repository contains a capstone analytics project focused on **labour market imbalance in Canada**.

The project studies the relationship between job vacancies, unemployment, labour force size, employment, population, and the vacancy-to-unemployment ratio, also referred to as **theta**.

The work follows a full analytics lifecycle:

1. Data collection and preparation.
2. Descriptive analysis.
3. Diagnostic analysis.
4. Predictive forecasting.
5. Model comparison and forecast evaluation.
6. Scenario-based interpretation for workforce planning.

The goal is to support evidence-based labour market planning by identifying patterns in unemployment, vacancies, and labour market tightness.

---

## 2. Business and Policy Problem

Canada’s labour market can experience mismatch when job vacancies and unemployment move in different directions. A high number of vacancies can exist at the same time as unemployment, which may indicate skill mismatch, regional mismatch, sectoral imbalance, or slower hiring adjustment.

This project analyzes that imbalance using historical labour market data and forecasting models.

The main analytical questions are:

- How have unemployment and job vacancies changed over time?
- When did labour market imbalance become more severe?
- How does the vacancy-to-unemployment ratio behave across labour market regimes?
- Which forecasting approach performs best for unemployment and vacancies?
- How can forecasted labour market conditions support workforce planning decisions?

---

## 3. Key Metric: Labour Market Tightness

The core imbalance measure in this project is:

```text
theta = job vacancies / unemployment
```

Interpretation:

- **Higher theta** means more vacancies relative to unemployed workers.
- **Lower theta** means fewer vacancies relative to unemployed workers.
- Changes in theta help identify labour market tightness and possible mismatch.

Important modeling rule used in the project:

> The predictive phase forecasts unemployment and vacancies first. Theta is then derived from those forecasts instead of being directly forecasted as the primary target.

This keeps the imbalance metric tied to its underlying economic components.

---

## 4. Repository Structure

```text
labour-market-imbalance-canada-capstone/
│
├── 0_proposal/                       # Proposal and planning documents
├── 1_data/
│   ├── raw/                          # Raw source datasets
│   └── processed/                    # Cleaned and modeling-ready datasets
│
├── 2_data_preparation/               # Data cleaning and alignment notebooks
├── 3_descriptive_diagnostic/          # Descriptive and diagnostic analysis notebooks
│   ├── exports/                      # Summary tables
│   └── figures/                      # Exported visuals
│
├── 4_predictive_forecasting/
│   ├── notebooks/                    # Forecasting notebooks
│   ├── exports/                      # Forecast outputs and evaluation tables
│   └── utils/                        # Forecasting helper scripts
│
├── 5_scenario_analysis/              # Scenario-based analysis outputs
├── src/labour_market_analytics/       # Reusable Python package utilities
├── scripts/                          # Runner scripts for validation and reproducibility
├── requirements.txt                   # Python package requirements
└── README.md
```

---

## 5. Data Files Used

The current repository includes processed modeling datasets such as:

- `1_data/processed/final_dataset_full.csv`
- `1_data/processed/final_dataset_modeling.csv`

The modeling dataset contains the core time-series fields used in the predictive phase:

- `month`
- `Employment`
- `Unemployment`
- `Labour force`
- `Population`
- `vacancies`
- `theta`

The missing COVID-period interval from April 2020 to September 2020 was removed before modeling to avoid distortion from a structurally abnormal gap.

---

## 6. Analytics Phases

### Phase 1: Data Preparation

The data preparation phase creates a clean monthly dataset for analysis and forecasting.

Main tasks:

- Load labour force and vacancy datasets.
- Standardize date fields.
- Align monthly time periods.
- Prepare employment, unemployment, labour force, population, vacancies, and theta fields.
- Export modeling-ready CSV files.

Relevant folder:

```text
2_data_preparation/
```

---

### Phase 2: Descriptive Analysis

The descriptive phase explains what happened in the labour market over time.

Main outputs include:

- Summary statistics.
- Missing data checks.
- Labour market trend charts.
- Theta trend analysis.
- Correlation heatmap.
- Beveridge curve visualizations.

Relevant folders:

```text
3_descriptive_diagnostic/
3_descriptive_diagnostic/exports/
3_descriptive_diagnostic/figures/
```

---

### Phase 3: Diagnostic Analysis

The diagnostic phase investigates why imbalance may have changed across periods.

Main tasks:

- Compare unemployment and vacancies.
- Examine labour market tightness using theta.
- Review structural change patterns.
- Support interpretation with diagnostic visuals and summary tables.

Relevant files:

```text
3_descriptive_diagnostic/descriptive.ipynb
3_descriptive_diagnostic/diagnostic.ipynb
```

---

### Phase 4: Predictive Forecasting

The predictive phase compares multiple forecasting approaches for unemployment and vacancies.

Current forecasting notebooks include:

- Stationarity and cointegration analysis.
- SARIMAX modeling.
- TBATS / Prophet-style benchmarking.
- LSTM attention modeling.
- Rolling-origin backtesting.
- Error diagnostics.
- Chronos benchmark.
- VAR modeling.
- Ensemble modeling.
- Final forecast generation.

Relevant folder:

```text
4_predictive_forecasting/notebooks/
```

---

## 7. Forecast Evaluation

The project evaluates forecasting performance using error metrics and model comparison tables.

Core evaluation metrics include:

- MAE
- RMSE
- MAPE
- Train R²
- Test R²
- Bias analysis
- Horizon-wise error comparison
- Model comparison by target variable

Reusable metric utilities were added in:

```text
src/labour_market_analytics/metrics.py
```

---

## 8. Reusable Code Added

This repository includes reusable Python utilities to make the project cleaner and easier to review.

### Data Validation

```text
src/labour_market_analytics/data_validation.py
```

This module supports:

- Loading the final modeling dataset.
- Checking required columns.
- Checking duplicate rows.
- Summarizing missing values.
- Reporting the available date range.
- Exporting a clean validation summary table.

### Forecast Metrics

```text
src/labour_market_analytics/metrics.py
```

This module supports:

- MAE calculation.
- RMSE calculation.
- MAPE calculation.
- R² calculation.
- Train-vs-test model summary table creation.
- Forecast error column generation.

### Validation Runner

```text
scripts/run_data_validation.py
```

Run from the repository root:

```bash
python scripts/run_data_validation.py
```

This exports:

```text
4_predictive_forecasting/exports/data_validation/modeling_dataset_validation_summary.csv
```

---

## 9. How to Run the Project

Clone the repository:

```bash
git clone https://github.com/poudelabhiyan/labour-market-imbalance-canada-capstone.git
cd labour-market-imbalance-canada-capstone
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the validation script:

```bash
python scripts/run_data_validation.py
```

Open notebooks using Jupyter:

```bash
jupyter notebook
```

---

## 10. Current Strengths of the Repository

This project demonstrates:

- End-to-end analytics project organization.
- Real labour market problem framing.
- Data cleaning and preparation.
- Descriptive and diagnostic analysis.
- Time-series forecasting workflow.
- Rolling-origin backtesting structure.
- Forecast comparison and final forecast outputs.
- Clear separation between notebooks, exports, figures, and reusable code.
- Practical business and policy interpretation.

---

## 11. Cleanup Notes for Future Improvement

Recommended cleanup before final portfolio sharing:

- Remove committed `__pycache__` files.
- Remove or replace empty output files.
- Standardize notebook names into a final numbered sequence.
- Add a final project report PDF when completed.
- Add a visual dashboard or executive summary page.
- Add source citations inside the report and final documentation.

---

## 12. Author

**Abhiyan Poudel**  
Master of Data Analytics student  
University of Niagara Falls Canada  
Focused on data analytics, workforce analytics, business intelligence, Python, SQL, Power BI, and forecasting.

GitHub: [poudelabhiyan](https://github.com/poudelabhiyan)
