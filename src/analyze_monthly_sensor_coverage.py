
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
)

# Extract year and month
df["year_month"] = df["timestamp"].dt.strftime("%Y-%m")

# Count observations for each sensor in each month
monthly_records = df.groupby(
    ["sensor_id", "year_month"]
).size().reset_index(name="record_count")

# Number of active sensors in each month
active_sensors = monthly_records.groupby(
    "year_month"
)["sensor_id"].nunique()

# Total observations in each month
total_records = monthly_records.groupby(
    "year_month"
)["record_count"].sum()

# Combine results
monthly_summary = pd.DataFrame({
    "active_sensors": active_sensors,
    "total_records": total_records
})

print("===== MONTHLY SENSOR COVERAGE =====")
print(monthly_summary.to_string())

print("\n===== COVERAGE SUMMARY =====")
print("Number of months:", len(monthly_summary))
print("Maximum active sensors:",
      monthly_summary["active_sensors"].max())
print("Minimum active sensors:",
      monthly_summary["active_sensors"].min())

# Save results
output_file = Path(
    "data/processed/monthly_sensor_coverage.csv"
)

monthly_summary.to_csv(output_file)

print("\nSaved to:", output_file)
print("\nAnalysis completed.")
