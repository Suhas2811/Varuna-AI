
from pathlib import Path
import pandas as pd

# Locate project directory
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data" / "raw"

csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("CSV file not found.")

# Load dataset
df = pd.read_csv(csv_files[0], sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Sort records by sensor and time
df = df.sort_values(["sensor_id", "timestamp"])

# 1. Records per sensor
print("\n===== SENSOR RECORD COUNTS =====")
print(df.groupby("sensor_id").size().describe())

# 2. Check timestamp gaps
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

print("\n===== TIME GAP DISTRIBUTION (MINUTES) =====")
print(df["time_gap_minutes"].describe())

print("\nMost common time gaps:")
print(df["time_gap_minutes"].value_counts().head(10))

# 3. Check duplicate sensor timestamps
duplicate_sensor_times = df.duplicated(
    subset=["sensor_id", "timestamp"]
).sum()

print("\n===== DUPLICATE SENSOR TIMESTAMPS =====")
print(duplicate_sensor_times)

# 4. Examine aggregated value changes
df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

print("\n===== AGGREGATED VALUE DIFFERENCES =====")
print(df["aggregated_difference"].describe())

print("\nNegative differences:")
print((df["aggregated_difference"] < 0).sum())

print("\nZero differences:")
print((df["aggregated_difference"] == 0).sum())

# 5. Show sample readings from one sensor
sample_sensor = df["sensor_id"].value_counts().index[0]

print("\n===== SAMPLE SENSOR READINGS =====")
print(
    df[df["sensor_id"] == sample_sensor][
        ["timestamp", "value", "aggregated_value"]
    ].head(15).to_string(index=False)
)

print("\n===== SENSOR ANALYSIS COMPLETED =====")
