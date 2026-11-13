
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

print("===== TIMESTAMP VALIDATION =====")

print("\nInvalid timestamps:", df["timestamp"].isna().sum())

print("\nTimestamp range:")
print("Minimum:", df["timestamp"].min())
print("Maximum:", df["timestamp"].max())

# Compare timestamp components with existing columns
print("\nDate mismatches:",
      (df["timestamp"].dt.strftime("%Y-%m-%d") != df["date"]).sum())

print("Hour mismatches:",
      (df["timestamp"].dt.hour != df["hour"]).sum())

print("Month mismatches:",
      (df["timestamp"].dt.month != df["month"]).sum())

print("Year mismatches:",
      (df["timestamp"].dt.year != df["year"]).sum())

print("\nTimestamp validation completed.")
