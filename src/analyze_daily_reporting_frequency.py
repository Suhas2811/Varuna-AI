
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

print("===== DAILY REPORTING FREQUENCY =====")

print("\nOverall daily records distribution:")
print(daily_counts["daily_records"].describe())

print("\nDays grouped by number of observations:")

print(
    pd.cut(
        daily_counts["daily_records"],
        bins=[0, 1, 5, 10, 20, 50, 100, float("inf")],
        labels=[
            "1", "2-5", "6-10", "11-20",
            "21-50", "51-100", "Above 100"
        ]
    ).value_counts().sort_index()
)

# Summarise daily reporting frequency per sensor
sensor_frequency = daily_counts.groupby("sensor_id").agg(
    active_days=("daily_records", "count"),
    average_daily_records=("daily_records", "mean"),
    median_daily_records=("daily_records", "median"),
    maximum_daily_records=("daily_records", "max")
)

print("\nPer-sensor daily reporting summary:")
print(sensor_frequency.describe())

print("\n10 sensors with lowest average daily records:")
print(
    sensor_frequency.sort_values(
        "average_daily_records"
    ).head(10)
)

output_file = Path(
    "data/processed/daily_reporting_frequency.csv"
)

sensor_frequency.to_csv(output_file)

print("\nSaved to:", output_file)
print("\nAnalysis completed.")
