
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "forecasting_daily_dataset.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "forecasting_features.csv"
)

# Load forecasting dataset
df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"], utc=True)

# Sort records sensor-wise and date-wise
df = df.sort_values(
    ["sensor_id", "date"]
).reset_index(drop=True)

# Calendar features
df["day_of_week"] = df["date"].dt.day_of_week
df["day_of_month"] = df["date"].dt.day
df["month"] = df["date"].dt.month

# Create lag and rolling features separately for each sensor
feature_frames = []

for sensor_id, group in df.groupby("sensor_id"):

    group = group.sort_values("date").copy()

    # Check consecutive dates
    date_gap = group["date"].diff().dt.days

    # Start a new segment after a missing day
    group["segment"] = date_gap.ne(1).cumsum()

    # Generate features within continuous segments
    for _, segment in group.groupby("segment"):

        segment = segment.copy()

        segment["lag_1"] = (
            segment["daily_consumption"].shift(1)
        )

        segment["lag_7"] = (
            segment["daily_consumption"].shift(7)
        )

        segment["rolling_mean_7"] = (
            segment["daily_consumption"]
            .shift(1)
            .rolling(window=7)
            .mean()
        )

        segment["rolling_mean_14"] = (
            segment["daily_consumption"]
            .shift(1)
            .rolling(window=14)
            .mean()
        )

        feature_frames.append(segment)

# Combine all sensor segments
features_df = pd.concat(
    feature_frames,
    ignore_index=True
)

# Save engineered dataset
features_df.to_csv(OUTPUT_FILE, index=False)

print("========== FEATURE ENGINEERING ==========")

print("\nTotal records:", len(features_df))
print("Unique sensors:", features_df["sensor_id"].nunique())

print("\nGenerated features:")
print([
    "day_of_week",
    "day_of_month",
    "month",
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_mean_14"
])

print("\nMissing values in engineered features:")
print(
    features_df[
        ["lag_1", "lag_7", "rolling_mean_7", "rolling_mean_14"]
    ].isnull().sum()
)

print("\nOutput saved successfully:")
print(OUTPUT_FILE)


print("\n========== FEATURE VALIDATION ==========")

print("\nDuplicate sensor-date records:")
print(
    features_df.duplicated(
        subset=["sensor_id", "date"]
    ).sum()
)

print("\nNegative lag values:")
print(
    (features_df["lag_1"].dropna() < 0).sum()
    + (features_df["lag_7"].dropna() < 0).sum()
)

print("\nFeature dataset shape:")
print(features_df.shape)

print("\nRecords available for modelling:")
model_df = features_df.dropna(
    subset=[
        "lag_1",
        "lag_7",
        "rolling_mean_7",
        "rolling_mean_14"
    ]
)
print(len(model_df))

print("\nRecords per sensor after removing incomplete features:")
print(model_df.groupby("sensor_id").size())

print("\nFeature validation completed.")
