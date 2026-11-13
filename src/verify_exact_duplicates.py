
import pandas as pd
from pathlib import Path

# Load original dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Identify exact duplicate rows
duplicates = df[df.duplicated(keep=False)].copy()

print("\n===== EXACT DUPLICATE INVESTIGATION =====")
print("Rows involved in exact duplicate groups:", len(duplicates))
print("Rows that would be removed using keep='first':",
      df.duplicated().sum())

print("\n===== SAMPLE EXACT DUPLICATES =====")
print(duplicates.head(20).to_string(index=False))

# Check duplicate groups
group_sizes = duplicates.groupby(
    list(df.columns),
    dropna=False
).size()

print("\n===== DUPLICATE GROUP SIZES =====")
print(group_sizes.value_counts().sort_index())

print("\n===== VERIFICATION COMPLETED =====")
