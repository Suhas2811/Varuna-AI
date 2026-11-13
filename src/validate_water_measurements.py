
from pathlib import Path
import pandas as pd

# Locate dataset
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data" / "raw"
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("Dataset not found.")

df = pd.read_csv(csv_files[0], sep=";", encoding="utf-8-sig")

# Sort by sensor and timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values(["sensor_id", "timestamp"]).copy()

# Calculate change in aggregated value per sensor
df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

# Compare the difference with value
df["difference_error"] = (
    df["aggregated_difference"] - df["value"]
)

print("\n===== AGGREGATED DIFFERENCE =====")
print(df["aggregated_difference"].describe())

print("\n===== NEGATIVE DIFFERENCES =====")
print((df["aggregated_difference"] < 0).sum())

print("\n===== ZERO DIFFERENCES =====")
print((df["aggregated_difference"] == 0).sum())

print("\n===== COMPARISON WITH VALUE =====")
print(df["difference_error"].describe())

print("\n===== CORRELATION =====")
print(
    df[["value", "aggregated_difference"]].corr()
)

# Show largest differences
print("\n===== LARGEST DIFFERENCES =====")
print(
    df.nlargest(10, "aggregated_difference")[
        ["sensor_id", "timestamp", "value",
         "aggregated_value", "aggregated_difference"]
    ].to_string(index=False)
)

# Show records with negative differences
print("\n===== NEGATIVE DIFFERENCE RECORDS =====")
print(
    df[df["aggregated_difference"] < 0][
        ["sensor_id", "timestamp", "value",
         "aggregated_value", "aggregated_difference"]
    ].to_string(index=False)
)

print("\n===== VALIDATION COMPLETED =====")
