
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

print("===== WATER VALUE VALIDATION =====")

for column in ["value", "aggregated_value"]:

    print(f"\n--- {column} ---")

    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())
    print("Mean:", df[column].mean())
    print("Median:", df[column].median())

    print("Negative values:", (df[column] < 0).sum())
    print("Zero values:", (df[column] == 0).sum())
    print("Missing values:", df[column].isna().sum())

    print("Values greater than 0.1:",
          (df[column] > 0.1).sum())

print("\nValidation completed.")
