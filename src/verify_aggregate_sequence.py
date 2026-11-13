
import pandas as pd
import numpy as np
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")
df["original_row"] = range(len(df))

# Identify repeated sensor-timestamp groups
repeated = df[
    df.duplicated(
        subset=["sensor_id", "timestamp"],
        keep=False
    )
].copy()

results = []

for (sensor, timestamp), group in repeated.groupby(
    ["sensor_id", "timestamp"],
    sort=False
):
    group = group.sort_values("original_row")

    values = group["value"].to_numpy()
    aggregates = group["aggregated_value"].to_numpy()

    aggregate_change = aggregates[-1] - aggregates[0]
    last_value = values[-1]

    results.append({
        "sensor_id": sensor,
        "timestamp": timestamp,
        "aggregate_change": aggregate_change,
        "last_value": last_value,
        "difference": aggregate_change - last_value
    })

result = pd.DataFrame(results)

print("\n===== AGGREGATE CHANGE VS LAST READING =====")

print("\nDifference statistics:")
print(result["difference"].describe().round(6))

print("\nMatches at different tolerances:")

for tolerance in [0.0005, 0.001, 0.002, 0.005]:
    matches = np.isclose(
        result["aggregate_change"],
        result["last_value"],
        atol=tolerance,
        rtol=0
    ).sum()

    print(f"Tolerance {tolerance}: {matches} / {len(result)}")

print("\n===== SAMPLE COMPARISON =====")
print(result.head(20).to_string(index=False))

print("\n===== INVESTIGATION COMPLETED =====")
