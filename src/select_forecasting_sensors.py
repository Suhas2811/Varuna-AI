
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
DAILY_FILE = DATA_PATH / "daily_sensor_consumption.csv"
COVERAGE_FILE = DATA_PATH / "sensor_daily_coverage.csv"

# Load previously generated files
daily_df = pd.read_csv(DAILY_FILE, parse_dates=["date"])
coverage_df = pd.read_csv(COVERAGE_FILE)

print("\n========== SENSOR COVERAGE ANALYSIS ==========")

# Coverage distribution
print("\nCoverage statistics:")
print(coverage_df["coverage_percent"].describe().round(2))

# Count sensors by coverage category
coverage_df["coverage_category"] = pd.cut(
    coverage_df["coverage_percent"],
    bins=[-1, 40, 60, 70, 80, 100],
    labels=[
        "Below 40%",
        "40-60%",
        "60-70%",
        "70-80%",
        "80-100%"
    ],
    include_lowest=True
)

print("\nSensors by coverage category:")
print(coverage_df["coverage_category"].value_counts().sort_index())

# Identify sensors meeting coverage thresholds
for threshold in [70, 80]:
    selected = coverage_df[
        (coverage_df["coverage_percent"] >= threshold)
        & (coverage_df["observed_days"] >= 180)
    ]

    print(f"\nSensors with at least {threshold}% coverage")
    print("Minimum 180 observed days")
    print("Number of sensors:", len(selected))
    print(selected[
        ["sensor_id", "observed_days", "coverage_percent"]
    ].to_string(index=False))

# Calculate longest consecutive observation streak
streak_results = []

for sensor, group in daily_df.groupby("sensor_id"):
    dates = (
        group["date"]
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    differences = dates.diff().dt.days.fillna(1)

    streak_id = differences.ne(1).cumsum()

    streak_lengths = dates.groupby(streak_id).size()

    streak_results.append({
        "sensor_id": sensor,
        "longest_consecutive_days": int(streak_lengths.max())
    })

streak_df = pd.DataFrame(streak_results)

# Combine coverage and streak information
sensor_selection = coverage_df.merge(
    streak_df,
    on="sensor_id",
    how="left"
)

print("\n========== CONTINUOUS DATA COVERAGE ==========")
print(
    sensor_selection["longest_consecutive_days"]
    .describe()
    .round(2)
)

# Save combined analysis
output_file = DATA_PATH / "forecasting_sensor_analysis.csv"

sensor_selection.to_csv(output_file, index=False)

print("\nAnalysis completed successfully.")
print("Saved:", output_file)


print("\n========== TOP SENSOR SHORTLIST ==========")

top_sensors = sensor_selection[
    (sensor_selection["coverage_percent"] >= 80)
    & (sensor_selection["observed_days"] >= 180)
].sort_values(
    by="longest_consecutive_days",
    ascending=False
)

print(
    top_sensors[
        [
            "sensor_id",
            "observed_days",
            "coverage_percent",
            "longest_consecutive_days"
        ]
    ].to_string(index=False)
)


# Inspect fixture information for shortlisted sensors

print("\n========== SHORTLISTED SENSOR DETAILS ==========")

RAW_DATA = DATA_PATH / "final_water_consumption.csv"

original_df = pd.read_csv(RAW_DATA)

sensor_details = (
    original_df[
        original_df["sensor_id"].isin(top_sensors["sensor_id"])
    ]
    .groupby("sensor_id")
    .agg(
        fixture=("attached_to", "first"),
        water_type=("type", "first"),
        room_type=("room_type", "first"),
        apartment=("apartment", "first"),
        cluster=("cluster_name", "first")
    )
    .reset_index()
)

final_shortlist = top_sensors.merge(
    sensor_details,
    on="sensor_id",
    how="left"
)

print(
    final_shortlist[
        [
            "sensor_id",
            "fixture",
            "water_type",
            "room_type",
            "coverage_percent",
            "longest_consecutive_days"
        ]
    ].to_string(index=False)
)

final_shortlist.to_csv(
    DATA_PATH / "final_sensor_shortlist.csv",
    index=False
)

print("\nShortlisted sensor details saved successfully.")
