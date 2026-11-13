
import pandas as pd
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

print("Original rows:", len(df))

# Remove only completely identical rows
df_cleaned = df.drop_duplicates().copy()

print("Rows after removing exact duplicates:", len(df_cleaned))
print("Rows removed:", len(df) - len(df_cleaned))

# Save cleaned dataset
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "water_consumption_cleaned.csv"

df_cleaned.to_csv(output_file, index=False)

print("\nCleaned dataset saved successfully!")
print("File:", output_file)
