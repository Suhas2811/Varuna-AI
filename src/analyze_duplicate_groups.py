
import pandas as pd
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Identify repeated sensor-timestamp groups
repeated = df[
    df.duplicated(
        subset=["sensor_id", "timestamp"],
        keep=False
    )
].copy()

# Sort records
repeated = repeated.sort_values(
    ["sensor_id", "timestamp"]
)

# Analyse repeated groups
group_summary = repeated.groupby(
    ["sensor_id", "timestamp"]
).agg(
    record_count=("value", "size"),
    unique_values=("value", "nunique"),
    unique_aggregates=("aggregated_value", "nunique"),
    total_value=("value", "sum"),
    minimum_value=("value", "min"),
    maximum_value=("value", "max")
).reset_index()

print("\n===== REPEATED GROUP ANALYSIS =====")
print("Total repeated groups:", len(group_summary))

print("\nRecords per group:")
print(group_summary["record_count"].value_counts().sort_index())

print("\nGroups with different measurement values:")
print((group_summary["unique_values"] > 1).sum())

print("\nGroups with different aggregated values:")
print((group_summary["unique_aggregates"] > 1).sum())

print("\n===== SAMPLE GROUPS WITH DIFFERENT VALUES =====")

different = group_summary[
    group_summary["unique_values"] > 1
]

sample_keys = different.head(15)[
    ["sensor_id", "timestamp"]
]

sample = repeated.merge(
    sample_keys,
    on=["sensor_id", "timestamp"]
)

print(sample.to_string(index=False))

print("\n===== INVESTIGATION COMPLETED =====")
