import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Sort observations
df = df.sort_values(["sensor_id", "timestamp"]).copy()

# Calculate time gaps
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Calculate aggregate differences
df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

# Select large differences
large = df[df["aggregated_difference"] > 1].copy()

# Extract date information
large["year"] = large["timestamp"].dt.year
large["month"] = large["timestamp"].dt.month
large["date"] = large["timestamp"].dt.date

print("\n===== LARGE DIFFERENCES BY MONTH =====")
print(
    large.groupby(["year", "month"])
    .size()
    .to_string()
)

print("\n===== LARGE DIFFERENCES BY DATE =====")
print(
    large.groupby("date")
    .size()
    .sort_values(ascending=False)
    .head(15)
    .to_string()
)

print("\n===== 2022 LARGE DIFFERENCES =====")
data_2022 = large[large["year"] == 2022]

print("Total:", len(data_2022))
print("Unique sensors:", data_2022["sensor_id"].nunique())
print("Unique dates:", data_2022["date"].nunique())

print("\n===== INVESTIGATION COMPLETED =====")
