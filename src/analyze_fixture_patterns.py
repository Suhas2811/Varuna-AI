
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# 1. Statistical analysis by fixture
fixture_stats = df.groupby("attached_to")["value"].agg(
    count="count",
    mean="mean",
    median="median",
    minimum="min",
    maximum="max",
    percentile_75=lambda x: x.quantile(0.75)
)

print("\n===== FIXTURE-WISE VALUE STATISTICS =====")
print(fixture_stats.round(4))

# 2. Mean value by fixture
plt.figure(figsize=(10, 5))
fixture_stats["mean"].sort_values(ascending=False).plot(kind="bar")

plt.title("Average Recorded Value by Fixture")
plt.xlabel("Fixture")
plt.ylabel("Mean Recorded Value (L)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("data/processed/fixture_mean_values.png")
plt.show()

# 3. Median value by fixture
plt.figure(figsize=(10, 5))
fixture_stats["median"].sort_values(ascending=False).plot(kind="bar")

plt.title("Median Recorded Value by Fixture")
plt.xlabel("Fixture")
plt.ylabel("Median Recorded Value (L)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("data/processed/fixture_median_values.png")
plt.show()

print("\n===== EDA STEP 3 COMPLETED =====")
