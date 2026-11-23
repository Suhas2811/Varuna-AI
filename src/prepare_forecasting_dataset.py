
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_water_consumption.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

# Seven shortlisted sensors
SELECTED_SENSORS = [
    "S0109",
    "S0102",
    "S0103",
    "S0107",
    "S0106",
    "S0105",
    "S0104"
]

# Load cleaned dataset
df = pd.read_csv(
    INPUT_FILE,
    sep=",",
    usecols=["timestamp", "sensor_id", "value", "attached_to", "type"]
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

# Filter selected sensors
df = df[df["sensor_id"].isin(SELECTED_SENSORS)].copy()

# Extract date
df["date"] = df["timestamp"].dt.floor("D")

# Aggregate daily consumption separately for each sensor
daily_df = (
    df.groupby(["sensor_id", "date"], as_index=False)
      .agg(
          daily_consumption=("value", "sum"),
          reading_count=("value", "count")
      )
)

# Sort chronologically
daily_df = daily_df.sort_values(
    ["sensor_id", "date"]
).reset_index(drop=True)

print("\n========== FORECASTING DATASET ==========")

print("Total sensor-day records:", len(daily_df))
print("Selected sensors:", daily_df["sensor_id"].nunique())

print("\nRecords per sensor:")
print(
    daily_df.groupby("sensor_id")
    .size()
    .to_string()
)

print("\nDaily consumption statistics:")
print(
    daily_df["daily_consumption"]
    .describe()
    .round(4)
)

# Check date gaps separately for each sensor
print("\n========== DATE GAP ANALYSIS ==========")

for sensor, group in daily_df.groupby("sensor_id"):

    dates = group["date"].sort_values()

    gaps = dates.diff().dt.days.dropna()

    print(f"\nSensor: {sensor}")
    print("Observed days:", len(dates))
    print("Longest gap (days):", int(gaps.max()) if len(gaps) else 0)
    print("Median gap (days):", gaps.median() if len(gaps) else 0)
    print("Days with gaps greater than 1:", int((gaps > 1).sum()))

# Save forecasting dataset
output_file = OUTPUT_DIR / "forecasting_daily_dataset.csv"

daily_df.to_csv(output_file, index=False)

print("\nForecasting dataset saved successfully.")
print("File:", output_file)


print("\n========== FORECASTING DATA VALIDATION ==========")

# Check missing values
print("\nMissing values:")
print(daily_df.isnull().sum())

# Check duplicate sensor-date combinations
print("\nDuplicate sensor-date records:")
print(
    daily_df.duplicated(
        subset=["sensor_id", "date"]
    ).sum()
)

# Check invalid consumption
print("\nNegative consumption records:")
print((daily_df["daily_consumption"] < 0).sum())

# Check sensor count
print("\nUnique sensors:")
print(daily_df["sensor_id"].nunique())

# Check date range
print("\nDate range:")
print(daily_df["date"].min())
print(daily_df["date"].max())

print("\nValidation completed.")
