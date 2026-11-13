
from pathlib import Path
import pandas as pd

# Locate dataset
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data" / "raw"

csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("Dataset not found.")

df = pd.read_csv(csv_files[0], sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Sort by sensor and timestamp
df = df.sort_values(["sensor_id", "timestamp"]).copy()

# Calculate time gaps
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Calculate aggregated differences
df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

# Compare differences with event values
df["difference_error"] = (
    df["aggregated_difference"] - df["value"]
)

# 1. Inspect large differences
print("\n===== LARGE AGGREGATED DIFFERENCES =====")

large = df.nlargest(15, "aggregated_difference")

print(
    large[
        ["sensor_id", "timestamp", "time_gap_minutes",
         "value", "aggregated_value",
         "aggregated_difference", "difference_error"]
    ].to_string(index=False)
)

# 2. Check differences greater than 1 litre
print("\n===== DIFFERENCES ABOVE 1 LITRE =====")
large_count = (df["aggregated_difference"] > 1).sum()
print("Count:", large_count)

# 3. Compare time gaps for large differences
print("\n===== TIME GAPS FOR LARGE DIFFERENCES =====")
print(
    df.loc[
        df["aggregated_difference"] > 1,
        "time_gap_minutes"
    ].describe()
)

# 4. Compare regular and irregular observation intervals
print("\n===== DIFFERENCE BY TIME GAP =====")

df["gap_category"] = pd.cut(
    df["time_gap_minutes"],
    bins=[0, 10, 30, 60, 180, float("inf")],
    labels=["Up to 10 min", "11-30 min",
            "31-60 min", "61-180 min", "Above 180 min"]
)

print(
    df.groupby("gap_category", observed=False)[
        "aggregated_difference"
    ].agg(["count", "mean", "median", "max"])
)

print("\n===== INVESTIGATION COMPLETED =====")
