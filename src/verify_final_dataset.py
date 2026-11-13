
import pandas as pd
from pathlib import Path

# Load final processed dataset
file_path = Path("data/processed/final_water_consumption.csv")

df = pd.read_csv(
    file_path,
    dtype={
        "apartment": "string",
        "cluster_name": "string"
    }
)

print("===== FINAL DATASET VERIFICATION =====")

# 1. Dataset dimensions
print("\nDataset shape:", df.shape)

# 2. Unique sensors
print("Unique sensors:", df["sensor_id"].nunique())

# 3. Check exact duplicates
print("Exact duplicates:", df.duplicated().sum())

# 4. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Check data types
print("\nColumn data types:")
print(df.dtypes)

# 6. Display column names
print("\nColumn names:")
print(df.columns.tolist())

# 7. Display first five records
print("\nFirst five records:")
print(df.head().to_string(index=False))

# 8. Final verification status
print("\n===== VERIFICATION SUMMARY =====")

if len(df) == 652175 and df.duplicated().sum() == 0:
    print("SUCCESS: Final dataset verification passed.")
else:
    print("WARNING: Please investigate the dataset.")

print("\nVerification completed.")
