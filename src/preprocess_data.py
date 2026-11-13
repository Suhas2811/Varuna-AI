
import pandas as pd
from pathlib import Path

# ==========================================
# 1. DEFINE PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

input_file = next(RAW_DIR.glob("*.csv"))

output_file = PROCESSED_DIR / "final_water_consumption.csv"
report_file = PROCESSED_DIR / "preprocessing_report.txt"

# ==========================================
# 2. LOAD ORIGINAL DATASET
# ==========================================

print("\n===== VARUNA AI PREPROCESSING =====")

df = pd.read_csv(
    input_file,
    sep=";",
    encoding="utf-8-sig"
)

original_rows = len(df)

print("Original records:", original_rows)

# ==========================================
# 3. REMOVE EXACT DUPLICATES
# ==========================================

duplicates_removed = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

print("Exact duplicates removed:", duplicates_removed)

# ==========================================
# 4. VALIDATE TIMESTAMPS
# ==========================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

invalid_timestamps = int(df["timestamp"].isna().sum())

if invalid_timestamps > 0:
    raise ValueError(
        "Invalid timestamps found. Preprocessing stopped."
    )

# ==========================================
# 5. VALIDATE MEASUREMENT VALUES
# ==========================================

measurement_columns = [
    "value",
    "aggregated_value"
]

for column in measurement_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if df[column].isna().any():
        raise ValueError(
            f"Invalid or missing values found in {column}."
        )

    if (df[column] < 0).any():
        raise ValueError(
            f"Negative values found in {column}."
        )

# ==========================================
# 6. SORT OBSERVATIONS
# ==========================================

df = df.sort_values(
    ["sensor_id", "timestamp"]
).reset_index(drop=True)

# ==========================================
# 7. SAVE PROCESSED DATASET
# ==========================================

df.to_csv(output_file, index=False)

# ==========================================
# 8. GENERATE PREPROCESSING REPORT
# ==========================================

report = f"""
VARUNA AI - PREPROCESSING REPORT

Original records: {original_rows}

Exact duplicate rows removed: {duplicates_removed}

Final records: {len(df)}

Total columns: {len(df.columns)}

Invalid timestamps: {invalid_timestamps}

Missing apartment values: {df['apartment'].isna().sum()}

Missing cluster values: {df['cluster_name'].isna().sum()}

Missing value measurements: {df['value'].isna().sum()}

Missing aggregated measurements: {df['aggregated_value'].isna().sum()}

Unique sensors: {df['sensor_id'].nunique()}

Final exact duplicates: {df.duplicated().sum()}

Preprocessing completed successfully.
"""

with open(report_file, "w", encoding="utf-8") as file:
    file.write(report)

print("\n===== PREPROCESSING RESULTS =====")
print(report)

print("Processed dataset:", output_file)
print("Report saved:", report_file)
