# AI-Driven Labour Market Imbalance Analysis — Canada

**Status:** Capstone portfolio project  
**Program:** Master of Data Analytics, University of Niagara Falls Canada  
**Target roles:** Data Analyst | BI Analyst | Workforce Analytics Analyst | Policy Data Analyst  
**Core tools:** Python, SQL, Power BI, Excel, GitHub, time-series forecasting, scenario analysis

---

## 1. Project Overview

This repository contains a capstone analytics project focused on **labour market imbalance in Canada** using Statistics Canada labour-market datasets.

The project studies the relationship between unemployment, job vacancies, labour force, employment, and population. The main imbalance measure is the **vacancy-to-unemployment ratio**, represented as `theta`.

The work follows a full analytics lifecycle:

1. Data preparation and validation
2. Descriptive and diagnostic analysis
3. Predictive forecasting
4. Scenario-based prescriptive analysis
5. Final reporting and business interpretation

The project is designed to support evidence-based workforce planning by showing where labour-market pressure is increasing, how imbalance may evolve, and how different vacancy or unemployment scenarios may affect future labour conditions.

---

## 2. Business Problem

Canada's labour market can face imbalance when job vacancies remain high while unemployment does not fall at the same rate, or when unemployment rises while vacancies weaken.

This creates practical questions for policy makers, employers, workforce planners, and analysts:

- Are labour shortages increasing or decreasing over time?
- How does unemployment move compared with job vacancies?
- Which labour-market signals give early warning of imbalance?
- Can future unemployment and vacancy levels be forecasted?
- How would labour imbalance change under different economic scenarios?

This project addresses those questions by building a structured analytics and forecasting workflow using official labour-market indicators.

---

## 3. Main Research Objective

The main objective is to analyze and forecast labour market imbalance in Canada using historical labour-market data and scenario-based analysis.

The project focuses on:

- Understanding trends in employment, unemployment, labour force, population, and job vacancies.
- Measuring imbalance using the vacancy-to-unemployment ratio.
- Forecasting unemployment and vacancies using time-series methods.
- Deriving future `theta` values from model outputs.
- Comparing multiple forecasting approaches using consistent evaluation metrics.
- Building scenario-based insights for workforce planning.

---

## 4. Dataset Scope

The modeling dataset is expected to include the following fields:

| Column | Meaning |
|---|---|
| `month` | Monthly date field |
| `Employment` | Number of employed persons |
| `Unemployment` | Number of unemployed persons |
| `Labour force` | Labour force count |
| `Population` | Population measure used in the project dataset |
| `vacancies` | Job vacancies |
| `theta` | Vacancy-to-unemployment ratio |

The project uses a monthly time-series structure. The final modeling phase forecasts **unemployment** and **vacancies** first. The `theta` ratio is derived only after base forecasts are produced.

---

## 5. Project Methodology

### Phase 1: Data Preparation

- Load raw labour-market datasets.
- Standardize date and geography fields.
- Aggregate data at the project-approved level.
- Merge datasets using common keys.
- Create the final modeling dataset.
- Validate missing values, duplicate records, date continuity, and numeric consistency.

### Phase 2: Descriptive and Diagnostic Analysis

- Analyze historical trends.
- Compare unemployment and vacancy movements.
- Examine labour-force and employment patterns.
- Study the behaviour of `theta` over time.
- Identify unusual periods and structural changes.

### Phase 3: Predictive Forecasting

Forecasting focuses on:

- Unemployment
- Job vacancies

Planned model families include:

- SARIMAX
- VAR / VECM
- Prophet / TBATS-style benchmark models
- Machine-learning benchmarks
- Ensemble comparison

Model evaluation is based on consistent rolling-origin validation and error metrics.

### Phase 4: Scenario-Based Prescriptive Analysis

The prescriptive phase is scenario-based. It does not use mathematical optimization.

Example scenario directions:

- Baseline continuation
- Higher vacancy pressure
- Lower vacancy pressure
- Higher unemployment pressure
- Combined imbalance stress case

Each scenario helps explain how labour-market imbalance may change under different assumptions.

---

## 6. Forecasting Evaluation Plan

The predictive phase will compare models using consistent metrics such as:

- RMSE
- MAE
- MAPE, where appropriate
- Train R²
- Test R²
- Residual diagnostics
- Rolling-origin validation results

A large difference between train and test performance will be treated as a possible overfitting signal. A smaller performance gap will be interpreted as stronger generalization.

---

## 7. Repository Structure

```text
labour-market-imbalance-canada-capstone/
│
├── 0_proposal/                    # Proposal documents and planning files
├── 1_data/                         # Raw, interim, and processed datasets
├── 2_data_preparation/             # Data cleaning and preparation workflow
├── 3_descriptive_diagnostic/        # Descriptive and diagnostic analysis
├── 4_predictive_forecasting/        # Forecasting notebooks, scripts, and outputs
├── 5_scenario_analysis/             # Scenario-based prescriptive analysis
│
├── src/                            # Reusable Python helper code
│   └── labour_market/
│       ├── __init__.py
│       ├── config.py
│       ├── data_quality.py
│       ├── features.py
│       └── metrics.py
│
├── scripts/                        # Runnable project scripts
│   └── run_data_quality_audit.py
│
├── README.md
└── requirements.txt
```

---

## 8. Code Added for Reproducibility

This repository includes reusable Python code for:

- Loading the final modeling dataset
- Validating required columns
- Checking missing values and duplicate rows
- Checking monthly date continuity
- Recalculating `theta`
- Creating lag features for forecasting
- Calculating common forecast evaluation metrics

These files support a cleaner professional workflow and make the project easier for reviewers to understand.

---

## 9. How to Run the Data Quality Audit

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the audit script from the project root:

```bash
python scripts/run_data_quality_audit.py --input 1_data/processed/final_dataset_modeling.csv --output 1_data/processed/data_quality_report.csv
```

The script checks:

- Dataset shape
- Required columns
- Missing values
- Duplicate rows
- Date parsing
- Monthly date continuity
- Basic numeric column quality

---

## 10. Portfolio Value

This project demonstrates:

- Labour-market data preparation
- Time-series thinking
- Data validation
- Forecasting workflow design
- Scenario-based business reasoning
- Clear documentation for non-technical readers
- Practical Python project structure
- GitHub portfolio readiness

The goal is not only to show code. The goal is to show how analytics can support labour-market planning and decision-making.

---

## 11. Author

**Abhiyan Poudel**  
Master of Data Analytics student  
Focused on data analytics, business intelligence, forecasting, and workforce analytics.

GitHub: [poudelabhiyan](https://github.com/poudelabhiyan)
