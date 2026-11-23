# Varuna AI

**Official Project Title:** Water Conservation Through Behavioural Nudges

Varuna AI is an academic Artificial Intelligence project focused on analysing water consumption patterns and developing data-driven approaches to encourage water conservation through behavioural nudges.

## Project Objectives

- Analyse water consumption patterns.
- Study usage across different water fixtures and sensors.
- Develop AI-based water consumption forecasting.
- Identify unusual and high-consumption patterns.
- Develop suitable behavioural nudge recommendations.
- Study Impact Scale, Income Sensitivity and Complementary Approach.

## Technology Stack

- Python 3.12
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Plotly
- Streamlit
- SQLite
- Google Colab
- VS Code and GitHub

## Dataset

The project uses the HSB Living Lab Fixture-Level Household Water Consumption Dataset.

- Source: HSB Living Lab, Gothenburg, Sweden.
- Original dataset: 652,315 records.
- Cleaned dataset: 652,175 records.
- Exact duplicate excess rows removed: 140.

Raw and processed CSV datasets are excluded from this repository.

**Data note:** The source documentation contains an inconsistency in the measurement unit of the `value` column. The unit is being verified before physical-unit claims are made.

## Project Progress

### Week 1 – Dataset Analysis and Preprocessing

- Dataset structure inspection.
- Exploratory data analysis.
- Missing-value investigation.
- Duplicate investigation and handling.
- Timestamp and measurement validation.
- Sensor coverage analysis.
- Preprocessing pipeline development.
- Final dataset verification.

**Result:** 652,175 cleaned records across 16 columns.

### Week 2 – AI/ML Development

**Forecasting**

- Daily consumption aggregation for seven selected sensors.
- Feature engineering using calendar, lag and rolling-statistic features.
- Linear Regression, Random Forest and Gradient Boosting model comparison.
- Persistence baseline comparison.
- Chronological 80:20 train-test split per sensor.
- Residual analysis and prediction evaluation.

**Best tested forecasting candidate:** Linear Regression with baseline features.

| Metric | Result |
|---|---:|
| MAE | 0.010993 |
| RMSE | 0.014759 |
| R² | 0.1111 |

These are unweighted averages of per-sensor metrics.

**Anomaly Detection**

- IQR statistical outlier detection.
- Basic Isolation Forest.
- Context-aware Isolation Forest.
- Rolling high-consumption threshold analysis.
- Consecutive alert sequence validation.

**Selected prototype high-consumption rule:**

`Threshold = Rolling Mean (7) + 2 × Rolling Standard Deviation (7)`

Results:

- Observations analysed: 6,194.
- High-consumption alerts: 422.
- Alert rate: 6.81%.
- Total alert sequences: 402.
- Multi-day alert sequences: 19.

These are exploratory alerts, not confirmed leakage or water-wastage incidents.

**Week 2 outputs:** Available under `reports/week2/`.

## Project Structure

```text
Varuna-AI/
├── data/
│   ├── raw/
│   └── processed/
├── database/
├── docs/
├── models/
├── notebooks/
├── pages/
├── reports/
│   └── week2/
├── src/
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/Suhas2811/Varuna-AI.git
cd Varuna-AI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Current Project Status

- Week 1: Dataset analysis and preprocessing completed.
- Week 2: Forecasting and anomaly-detection experiments completed.
- Week 3: Behavioural nudge intelligence – upcoming.
- Week 4: Application integration, testing and documentation – upcoming.

## Limitations

- Anomaly detections are not supported by verified ground-truth labels.
- Forecasting performance varies across sensors.
- Forecasting alone does not establish water savings.
- Nudge effectiveness requires appropriate intervention and outcome evaluation.

## Academic Project

**Project:** Water Conservation Through Behavioural Nudges

**Application Name:** Varuna AI