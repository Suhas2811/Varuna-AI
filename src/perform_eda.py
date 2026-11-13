
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Create month column
df["month"] = df["timestamp"].dt.strftime("%Y-%m")

# 1. Monthly record distribution
monthly = df.groupby("month").size()

plt.figure(figsize=(12, 5))
monthly.plot(kind="bar")
plt.title("Monthly Water Consumption Records")
plt.xlabel("Month")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/processed/monthly_records.png")
plt.show()

# 2. Fixture distribution
fixture_counts = df["attached_to"].value_counts()

plt.figure(figsize=(9, 5))
fixture_counts.plot(kind="bar")
plt.title("Records by Water Fixture")
plt.xlabel("Fixture")
plt.ylabel("Number of Records")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("data/processed/fixture_distribution.png")
plt.show()

# 3. Water type distribution
water_counts = df["type"].value_counts()

plt.figure(figsize=(7, 5))
water_counts.plot(kind="bar")
plt.title("Hot and Cold Water Records")
plt.xlabel("Water Type")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("data/processed/water_type_distribution.png")
plt.show()

print("\n===== MONTHLY RECORDS =====")
print(monthly)

print("\n===== FIXTURE DISTRIBUTION =====")
print(fixture_counts)

print("\n===== WATER TYPE DISTRIBUTION =====")
print(water_counts)

print("\n===== EDA STEP 1 COMPLETED =====")
