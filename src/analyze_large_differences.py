
import pandas as pd
from pathlib import Path

# Locate dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

# Load dataset
df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Sort records
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

# Identify large differences
large = df[df["aggregated_difference"] > 1].copy()

print("\n===== LARGE DIFFERENCES BY FIXTURE =====")
print(large["attached_to"].value_counts())

print("\n===== LARGE DIFFERENCES BY WATER TYPE =====")
print(large["type"].value_counts())

print("\n===== LARGE DIFFERENCES BY YEAR =====")
print(large["timestamp"].dt.year.value_counts().sort_index())

print("\n===== LARGE DIFFERENCES BY SENSOR =====")
print(large["sensor_id"].value_counts().head(15))

print("\n===== LARGEST DIFFERENCES WITH SENSOR DETAILS =====")
columns = [
    "sensor_id",
    "timestamp",
    "attached_to",
    "type",
    "apartment",
    "time_gap_minutes",
    "value",
    "aggregated_difference"
]

print(
    large.nlargest(15, "aggregated_difference")[columns]
    .to_string(index=False)
)

print("\n===== INVESTIGATION COMPLETED =====")
