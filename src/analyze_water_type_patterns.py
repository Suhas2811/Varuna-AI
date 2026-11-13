
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# 1. Record counts by fixture and water type
counts = pd.crosstab(
    df["attached_to"],
    df["type"]
)

print("\n===== RECORD COUNTS BY FIXTURE AND WATER TYPE =====")
print(counts)

# 2. Average recorded value by fixture and water type
means = df.pivot_table(
    index="attached_to",
    columns="type",
    values="value",
    aggfunc="mean"
)

print("\n===== MEAN VALUE BY FIXTURE AND WATER TYPE =====")
print(means.round(4))

# 3. Visualize record counts
counts.plot(kind="bar", figsize=(11, 6))

plt.title("Hot and Cold Water Records by Fixture")
plt.xlabel("Fixture")
plt.ylabel("Number of Records")
plt.xticks(rotation=30)
plt.legend(title="Water Type")
plt.tight_layout()
plt.savefig("data/processed/water_type_by_fixture.png")
plt.show()

# 4. Visualize average recorded values
means.plot(kind="bar", figsize=(11, 6))

plt.title("Average Recorded Value by Fixture and Water Type")
plt.xlabel("Fixture")
plt.ylabel("Mean Recorded Value (L)")
plt.xticks(rotation=30)
plt.legend(title="Water Type")
plt.tight_layout()
plt.savefig("data/processed/mean_water_type_by_fixture.png")
plt.show()

print("\n===== EDA STEP 4 COMPLETED =====")
