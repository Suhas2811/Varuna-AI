
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "final_water_consumption.csv"

# Load processed dataset
df = pd.read_csv(DATA_PATH)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

print("\n========== DATASET INFORMATION ==========")
print("Total records:", len(df))
print("Unique sensors:", df["sensor_id"].nunique())
print("Date range:", df["timestamp"].min(), "to", df["timestamp"].max())

# Create daily consumption totals for each sensor
daily_data = (
    df.groupby(["sensor_id", "date"], as_index=False)
      .agg(
          daily_consumption=("value", "sum"),
          reading_count=("value", "count")
      )
)

daily_data["date"] = pd.to_datetime(daily_data["date"])

print("\n========== DAILY DATA SUMMARY ==========")
print("Total sensor-day records:", len(daily_data))
print("Unique sensors:", daily_data["sensor_id"].nunique())
print("Average daily consumption:", daily_data["daily_consumption"].mean())
print("Median daily consumption:", daily_data["daily_consumption"].median())

# Check daily reporting coverage
daily_data["year_month"] = daily_data["date"].dt.to_period("M")

monthly_coverage = (
    daily_data.groupby("year_month")
    .agg(
        active_sensors=("sensor_id", "nunique"),
        sensor_days=("sensor_id", "count")
    )
)

print("\n========== MONTHLY COVERAGE ==========")
print(monthly_coverage.to_string())

# Check missing calendar dates for each sensor
coverage_results = []

for sensor, group in daily_data.groupby("sensor_id"):
    dates = group["date"].sort_values()

    expected_days = (
        (dates.max() - dates.min()).days + 1
    )

    observed_days = dates.nunique()
    missing_days = expected_days - observed_days

    coverage_results.append({
        "sensor_id": sensor,
        "expected_days": expected_days,
        "observed_days": observed_days,
        "missing_days": missing_days,
        "coverage_percent": round(
            observed_days / expected_days * 100, 2
        )
    })

coverage_df = pd.DataFrame(coverage_results)

print("\n========== SENSOR DAILY COVERAGE ==========")
print(coverage_df.describe().round(2))

# Save inspection outputs
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed"

daily_data.to_csv(
    OUTPUT_PATH / "daily_sensor_consumption.csv",
    index=False
)

coverage_df.to_csv(
    OUTPUT_PATH / "sensor_daily_coverage.csv",
    index=False
)

print("\nInspection completed successfully.")
print("Output files saved in data/processed/")
