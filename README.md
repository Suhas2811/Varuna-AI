# Varuna AI

**Official Project Title:** Water Conservation Through Behavioural Nudges

Varuna AI is an academic Artificial Intelligence project focused on analysing water consumption patterns and developing data-driven approaches to encourage water conservation through behavioural nudges.

## Project Objectives

- Analyse water consumption patterns.
- Study usage across different water fixtures and sensors.
- Explore AI-based water consumption prediction.
- Identify unusual consumption patterns for further investigation.
- Develop suitable behavioural nudge recommendations.
- Study impact scale, income sensitivity and complementary approaches.

## Technology Stack

- Python 3.12
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Plotly
- Streamlit
- SQLite

## Dataset

The project uses the HSB Living Lab Fixture-Level Household Water Consumption Dataset.

The dataset contains anonymised household water-meter observations from Gothenburg, Sweden.

Raw and processed CSV datasets are not included in this repository. Refer to the original dataset source and its documentation before using the data.

## Current Progress

### Week 1 – Dataset Analysis and Preprocessing

- Dataset structure inspection
- Exploratory data analysis
- Missing-value investigation
- Duplicate investigation and handling
- Timestamp and measurement validation
- Sensor coverage analysis
- Preprocessing pipeline development
- Final dataset verification

**Processed dataset:** 652,175 records and 16 columns.

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
├── src/
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd Varuna-AI
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

## Project Status

Currently under development. AI modelling, behavioural nudge implementation and application development are planned for subsequent phases.

## Academic Project

**Project:** Water Conservation Through Behavioural Nudges  
**Application Name:** Varuna AI