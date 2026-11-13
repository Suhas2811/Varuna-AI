
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/water_consumption_cleaned.csv")
df = pd.read_csv(file_path)

print("===== MISSING VALUE INVESTIGATION =====")

print("\n1. Missing values by room type:")
print(
    df[df["apartment"].isna()]
    ["room_type"]
    .value_counts(dropna=False)
)

print("\n2. Missing apartment by room type:")
print(
    pd.crosstab(
        df["room_type"],
        df["apartment"].isna(),
        margins=True
    )
)

print("\n3. Missing cluster by room type:")
print(
    pd.crosstab(
        df["room_type"],
        df["cluster_name"].isna(),
        margins=True
    )
)

print("\n4. Missing apartment and cluster together:")
print(
    df[["apartment", "cluster_name"]]
    .isna()
    .value_counts()
)

print("\nInvestigation completed.")

