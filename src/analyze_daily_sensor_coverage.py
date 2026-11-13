
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

# Extract calendar date
df["observation_date"] = df["timestamp"].dt.date

# Count distinct days with observations for each sensor
daily_activity = df.groupby("sensor_id").agg(
    active_days=("observation_date", "nunique"),
    total_records=("timestamp", "count")
)

print("===== DAILY SENSOR COVERAGE =====")

print("\nActive days distribution:")
print(daily_activity["active_days"].describe())

print("\nSensors grouped by active days:")

print(
    pd.cut(
        daily_activity["active_days"],
        bins=[0, 30, 100, 300, 600, 1200],
        labels=["1-30", "31-100", "101-300",
                "301-600", "601-1200"]
    ).value_counts().sort_index()
)

print("\n10 sensors with the fewest active days:")
print(
    daily_activity.sort_values("active_days").head(10)
)

print("\n10 sensors with the most active days:")
print(
    daily_activity.sort_values(
        "active_days", ascending=False
    ).head(10)
)

output_file = Path(
    "data/processed/daily_sensor_coverage.csv"
)

daily_activity.to_csv(output_file)

print("\nSaved to:", output_file)
print("\nAnalysis completed.")
