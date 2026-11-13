
from pathlib import Path
import pandas as pd

# Locate project and dataset
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data" / "raw"
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("Dataset not found.")

df = pd.read_csv(csv_files[0], sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Extract calendar date
df["date"] = df["timestamp"].dt.date

# Sort records
df = df.sort_values(["sensor_id", "timestamp"])

# 1. Daily record counts
print("\n===== DAILY RECORD COUNTS =====")
daily_records = df.groupby("date").size()
print(daily_records.describe())

# 2. Daily sum of value
print("\n===== DAILY VALUE SUM =====")
daily_value = df.groupby("date")["value"].sum()
print(daily_value.describe())

# 3. Daily sum of aggregated_value
print("\n===== DAILY AGGREGATED VALUE SUM =====")
daily_aggregated = df.groupby("date")["aggregated_value"].sum()
print(daily_aggregated.describe())

# 4. Daily sensor coverage
print("\n===== DAILY SENSOR COVERAGE =====")
daily_sensors = df.groupby("date")["sensor_id"].nunique()
print(daily_sensors.describe())

# 5. Sample daily results
print("\n===== FIRST 15 DAILY RECORDS =====")
daily_summary = pd.DataFrame({
    "records": daily_records,
    "value_sum": daily_value,
    "aggregated_sum": daily_aggregated,
    "unique_sensors": daily_sensors
})

print(daily_summary.head(15))

print("\n===== DAILY ANALYSIS COMPLETED =====")
