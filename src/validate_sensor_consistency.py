
import pandas as pd
from pathlib import Path

# Load cleaned dataset
file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

print("===== SENSOR CONSISTENCY VALIDATION =====")

# Sort observations by sensor and timestamp
df = df.sort_values(["sensor_id", "timestamp"])

# 1. Records per sensor
sensor_summary = df.groupby("sensor_id").agg(
    record_count=("timestamp", "count"),
    first_observation=("timestamp", "min"),
    last_observation=("timestamp", "max"),
    fixture_types=("attached_to", "nunique"),
    water_types=("type", "nunique")
)

print("\n1. SENSOR RECORD SUMMARY")
print(sensor_summary["record_count"].describe())

print("\nSensors with only one record:",
      (sensor_summary["record_count"] == 1).sum())

print("\nSensors with multiple fixture types:",
      (sensor_summary["fixture_types"] > 1).sum())

print("\nSensors with multiple water types:",
      (sensor_summary["water_types"] > 1).sum())

# 2. Time gaps between observations
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

gap_summary = df.groupby("sensor_id")["time_gap_minutes"].agg(
    median_gap="median",
    maximum_gap="max"
)

sensor_summary = sensor_summary.join(gap_summary)

print("\n2. TIME GAP SUMMARY (MINUTES)")
print(sensor_summary[["median_gap", "maximum_gap"]].describe())

# 3. Repeated timestamps per sensor
repeated = df.duplicated(
    subset=["sensor_id", "timestamp"],
    keep=False
)

print("\n3. REPEATED SENSOR-TIMESTAMP RECORDS")
print("Rows involved:", repeated.sum())
print("Repeated groups:",
      df.loc[repeated].groupby(
          ["sensor_id", "timestamp"]
      ).ngroups)

# 4. Show sensors with the fewest records
print("\n4. SENSORS WITH FEWEST RECORDS")
print(sensor_summary.sort_values("record_count").head(10))

# 5. Save sensor summary
output_file = Path("data/processed/sensor_summary.csv")
sensor_summary.to_csv(output_file)

print("\nSensor summary saved to:", output_file)
print("\nValidation completed.")
