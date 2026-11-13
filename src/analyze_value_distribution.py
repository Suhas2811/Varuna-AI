
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Overall value statistics
print("\n===== OVERALL VALUE DISTRIBUTION =====")
print(df["value"].describe())

# Value distribution by fixture
print("\n===== VALUE BY FIXTURE =====")
print(
    df.groupby("attached_to")["value"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(4)
)

# Value distribution by water type
print("\n===== VALUE BY WATER TYPE =====")
print(
    df.groupby("type")["value"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(4)
)

# Check unusually high values
print("\n===== VALUES ABOVE 0.05 L =====")
print("Count:", (df["value"] > 0.05).sum())

print("\n===== VALUES ABOVE 0.10 L =====")
print("Count:", (df["value"] > 0.10).sum())

print("\n===== HIGHEST 15 VALUES =====")
print(
    df.nlargest(15, "value")[
        ["timestamp", "sensor_id", "attached_to",
         "type", "value", "aggregated_value"]
    ].to_string(index=False)
)

print("\n===== INVESTIGATION COMPLETED =====")
