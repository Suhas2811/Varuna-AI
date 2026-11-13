
import pandas as pd
import numpy as np
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Preserve original row order
df["original_row"] = range(len(df))

# Identify repeated sensor-timestamp groups
repeated = df[
    df.duplicated(
        subset=["sensor_id", "timestamp"],
        keep=False
    )
].copy()

# Analyse each group
results = []

for (sensor, timestamp), group in repeated.groupby(
    ["sensor_id", "timestamp"],
    sort=False
):
    group = group.sort_values("original_row")

    values = group["value"].to_numpy()
    aggregates = group["aggregated_value"].to_numpy()

    aggregate_change = aggregates[-1] - aggregates[0]
    total_value = values.sum()

    results.append({
        "sensor_id": sensor,
        "timestamp": timestamp,
        "records": len(group),
        "total_value": total_value,
        "aggregate_change": aggregate_change,
        "difference": aggregate_change - total_value,
        "aggregates_monotonic": np.all(np.diff(aggregates) >= 0),
        "exact_duplicate_inside_group": group.duplicated(
            subset=df.columns.drop("original_row").tolist()
        ).any()
    })

summary = pd.DataFrame(results)

print("\n===== MEASUREMENT SEQUENCE ANALYSIS =====")
print("Total groups:", len(summary))

print("\nAggregate values monotonic:")
print(summary["aggregates_monotonic"].value_counts())

print("\nGroups with matching aggregate change and total value:")
matching = np.isclose(
    summary["aggregate_change"],
    summary["total_value"],
    atol=0.001
)
print(matching.sum())

print("\nDifference between aggregate change and total value:")
print(summary["difference"].describe().round(6))

print("\nGroups containing exact duplicate rows:")
print(summary["exact_duplicate_inside_group"].sum())

print("\n===== SAMPLE GROUP COMPARISON =====")
print(
    summary.head(20).to_string(index=False)
)

print("\n===== INVESTIGATION COMPLETED =====")
