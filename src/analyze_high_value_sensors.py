
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Select high-value records
high = df[df["value"] > 0.10].copy()

print("\n===== HIGH VALUE SENSOR ANALYSIS =====")

print("Total high-value records:", len(high))
print("Unique sensors:", high["sensor_id"].nunique())

print("\n===== TOP 15 SENSORS =====")

print(
    high.groupby("sensor_id")
    .agg(
        high_value_count=("value", "count"),
        average_value=("value", "mean"),
        maximum_value=("value", "max"),
        fixture=("attached_to", "first")
    )
    .sort_values("high_value_count", ascending=False)
    .head(15)
    .round(4)
)

print("\n===== HIGH VALUE COUNTS BY SENSOR =====")

sensor_counts = high.groupby("sensor_id").size()

print(sensor_counts.describe())

print("\n===== INVESTIGATION COMPLETED =====")
