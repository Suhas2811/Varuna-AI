
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")

df = pd.read_csv(file_path)

print("===== CLEANED DATASET VERIFICATION =====")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nRemaining exact duplicates:", df.duplicated().sum())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset shape:", df.shape)

print("\nVerification completed.")
