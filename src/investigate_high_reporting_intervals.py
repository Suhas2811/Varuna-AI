
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

df["observation_date"] = df["timestamp"].dt.date

# Count observations per sensor per day
daily_counts = df.groupby(
    ["sensor_id", "observation_date"]
).size().reset_index(name="daily_records")

# Select sensor-days with more than 50 records
high_days = daily_counts[
    daily_counts["daily_records"] > 50
][["sensor_id", "observation_date"]]

# Get observations belonging to these sensor-days
selected = df.merge(
    high_days,
    on=["sensor_id", "observation_date"],
    how="inner"
)

selected = selected.sort_values(
    ["sensor_id", "timestamp"]
)

# Calculate time gaps between consecutive observations
selected["gap_minutes"] = (
    selected.groupby(
        ["sensor_id", "observation_date"]
    )["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Summarise intervals
summary = selected.groupby(
    ["sensor_id", "observation_date"]
).agg(
    records=("timestamp", "count"),
    minimum_gap=("gap_minutes", "min"),
    median_gap=("gap_minutes", "median"),
    maximum_gap=("gap_minutes", "max")
).reset_index()

print("===== HIGH REPORTING INTERVAL ANALYSIS =====")
print(summary.to_string(index=False))

output_file = Path(
    "data/processed/high_reporting_intervals.csv"
)

summary.to_csv(output_file, index=False)

print("\nSaved to:", output_file)
print("\nAnalysis completed.")
