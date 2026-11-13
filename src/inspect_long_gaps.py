
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Convert timestamp and sort records
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values(["sensor_id", "timestamp"]).copy()

# Calculate time gaps and aggregate differences
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

# Select observations after gaps longer than 30 days
long_gaps = df[df["time_gap_minutes"] > 30 * 24 * 60].copy()

print("\n===== OBSERVATIONS AFTER GAPS LONGER THAN 30 DAYS =====")
print("Total records:", len(long_gaps))
print("Unique sensors:", long_gaps["sensor_id"].nunique())

# Display the 15 largest gaps
print("\n===== 15 LARGEST GAPS =====")

columns = [
    "sensor_id",
    "timestamp",
    "attached_to",
    "time_gap_minutes",
    "value",
    "aggregated_value",
    "aggregated_difference"
]

print(
    long_gaps.nlargest(15, "time_gap_minutes")[columns]
    .to_string(index=False)
)

print("\n===== AGGREGATE DIFFERENCE SUMMARY =====")
print(long_gaps["aggregated_difference"].describe())

print("\n===== INVESTIGATION COMPLETED =====")
