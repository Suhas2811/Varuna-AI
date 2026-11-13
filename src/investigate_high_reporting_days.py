
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

df["observation_date"] = df["timestamp"].dt.date

# Count records per sensor per day
daily_counts = df.groupby(
    ["sensor_id", "observation_date"]
).size().reset_index(name="daily_records")

# Identify days with more than 50 observations
high_days = daily_counts[
    daily_counts["daily_records"] > 50
].sort_values("daily_records", ascending=False)

print("===== HIGH REPORTING DAY INVESTIGATION =====")

print("\nNumber of sensor-days above 50 records:",
      len(high_days))

print("\nHigh reporting days:")
print(high_days.to_string(index=False))

print("\nSensors involved:")
print(high_days["sensor_id"].value_counts())

print("\nMaximum daily records:",
      high_days["daily_records"].max())

output_file = Path(
    "data/processed/high_reporting_days.csv"
)

high_days.to_csv(output_file, index=False)

print("\nSaved to:", output_file)
print("\nInvestigation completed.")
