
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/sensor_summary.csv")
df = pd.read_csv(file_path)

# Classify sensors based on record count
def classify_sensor(count):
    if count < 100:
        return "Very Low"
    elif count < 1000:
        return "Low"
    elif count < 5000:
        return "Moderate"
    else:
        return "High"

df["coverage_category"] = df["record_count"].apply(
    classify_sensor
)

print("===== SENSOR COVERAGE CLASSIFICATION =====")

print("\nSensors in each category:")
print(df["coverage_category"].value_counts())

print("\nPercentage distribution:")
print(
    (df["coverage_category"].value_counts(normalize=True) * 100)
    .round(2)
)

print("\nSensors with very low coverage:")
print(
    df[df["coverage_category"] == "Very Low"][
        ["sensor_id", "record_count",
         "first_observation", "last_observation"]
    ].to_string(index=False)
)

# Save classification
output_file = Path(
    "data/processed/sensor_coverage_classification.csv"
)

df.to_csv(output_file, index=False)

print("\nClassification saved to:", output_file)
print("\nCompleted.")

