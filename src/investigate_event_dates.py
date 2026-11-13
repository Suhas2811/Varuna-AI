
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values(["sensor_id", "timestamp"]).copy()

# Calculate gaps and aggregate differences
df["time_gap_minutes"] = (
    df.groupby("sensor_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

df["aggregated_difference"] = (
    df.groupby("sensor_id")["aggregated_value"].diff()
)

# Investigate the two major dates
target_dates = ["2022-02-23", "2022-10-06"]

for target in target_dates:

    print(f"\n===== INVESTIGATION: {target} =====")

    event_date = pd.Timestamp(target, tz="UTC")

    # Select records within one day before and after
    period = df[
        (df["timestamp"] >= event_date - pd.Timedelta(days=1)) &
        (df["timestamp"] < event_date + pd.Timedelta(days=2))
    ]

    print("Total records:", len(period))
    print("Unique sensors:", period["sensor_id"].nunique())

    print("\nRecords per day:")
    print(period.groupby(period["timestamp"].dt.date).size())

    print("\nMedian time gap:", period["time_gap_minutes"].median())
    print("Maximum time gap:", period["time_gap_minutes"].max())

    print("\nLarge differences:")
    print((period["aggregated_difference"] > 1).sum())

    print("\nSensors with large differences:")
    print(
        period.loc[
            period["aggregated_difference"] > 1,
            "sensor_id"
        ].unique()
    )

print("\n===== INVESTIGATION COMPLETED =====")
