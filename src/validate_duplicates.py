
import pandas as pd
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

print("\n===== ORIGINAL DATASET =====")
print("Total records:", len(df))

# 1. Check exact duplicate rows
exact_duplicates = df.duplicated().sum()

print("\n===== EXACT DUPLICATES =====")
print("Duplicate rows:", exact_duplicates)

# 2. Check repeated sensor-timestamp combinations
sensor_timestamp_duplicates = df.duplicated(
    subset=["sensor_id", "timestamp"]
).sum()

print("\n===== SENSOR-TIMESTAMP DUPLICATES =====")
print("Repeated records:", sensor_timestamp_duplicates)

# 3. Inspect repeated sensor-timestamp records
repeated = df[
    df.duplicated(
        subset=["sensor_id", "timestamp"],
        keep=False
    )
].sort_values(["sensor_id", "timestamp"])

print("\n===== SAMPLE REPEATED RECORDS =====")
print(repeated.head(20).to_string(index=False))

# 4. Check whether repeated records have different values
duplicate_groups = repeated.groupby(
    ["sensor_id", "timestamp"]
).size()

print("\n===== DUPLICATE GROUP SUMMARY =====")
print("Repeated groups:", len(duplicate_groups))
print("Largest group size:", duplicate_groups.max())

print("\n===== VALIDATION COMPLETED =====")
