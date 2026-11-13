
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df["month"] = df["timestamp"].dt.strftime("%Y-%m")

# 1. Records contributed by each sensor
sensor_counts = df.groupby("sensor_id").size().sort_values(
    ascending=False
)

print("\n===== SENSOR COVERAGE =====")
print("Total sensors:", df["sensor_id"].nunique())
print("Minimum records per sensor:", sensor_counts.min())
print("Maximum records per sensor:", sensor_counts.max())
print("\nTop 10 sensors:")
print(sensor_counts.head(10))

# 2. Active sensors per month
monthly_sensors = df.groupby("month")["sensor_id"].nunique()

print("\n===== MONTHLY ACTIVE SENSORS =====")
print(monthly_sensors)

plt.figure(figsize=(12, 5))
monthly_sensors.plot(kind="bar")
plt.title("Number of Active Sensors per Month")
plt.xlabel("Month")
plt.ylabel("Number of Sensors")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/processed/monthly_active_sensors.png")
plt.show()

# 3. Records by apartment
apartment_counts = df["apartment"].value_counts()

print("\n===== APARTMENT COVERAGE =====")
print("Total apartments:", df["apartment"].nunique())
print("Records without apartment:", df["apartment"].isna().sum())
print("\nRecords by apartment:")
print(apartment_counts)

plt.figure(figsize=(12, 5))
apartment_counts.sort_index().plot(kind="bar")
plt.title("Records by Apartment")
plt.xlabel("Apartment")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/processed/apartment_distribution.png")
plt.show()

# 4. Missing apartment and cluster information
print("\n===== MISSING ASSIGNMENTS =====")
print("Missing apartment:", df["apartment"].isna().sum())
print("Missing cluster:", df["cluster_name"].isna().sum())

print("\n===== EDA STEP 5 COMPLETED =====")
