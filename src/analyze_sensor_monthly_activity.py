
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

df["year_month"] = df["timestamp"].dt.to_period("M")

# Count distinct active months for each sensor
sensor_activity = df.groupby("sensor_id").agg(
    active_months=("year_month", "nunique"),
    total_records=("timestamp", "count"),
    first_observation=("timestamp", "min"),
    last_observation=("timestamp", "max")
)

print("===== SENSOR MONTHLY ACTIVITY =====")

print("\nActive month distribution:")
print(sensor_activity["active_months"].describe())

print("\nSensors grouped by active months:")

print(
    pd.cut(
        sensor_activity["active_months"],
        bins=[0, 5, 10, 20, 30, 50],
        labels=["1-5", "6-10", "11-20", "21-30", "31+"]
    ).value_counts().sort_index()
)

print("\n10 sensors with the fewest active months:")
print(
    sensor_activity.sort_values("active_months").head(10)
)

print("\n10 sensors with the most active months:")
print(
    sensor_activity.sort_values(
        "active_months", ascending=False
    ).head(10)
)

output_file = Path(
    "data/processed/sensor_monthly_activity.csv"
)

sensor_activity.to_csv(output_file)

print("\nSaved to:", output_file)
print("\nAnalysis completed.")
