
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Extract time features
df["hour"] = df["timestamp"].dt.hour
df["day_name"] = df["timestamp"].dt.day_name()

# 1. Hourly record distribution
hourly = df.groupby("hour").size()

plt.figure(figsize=(10, 5))
hourly.plot(kind="bar")
plt.title("Hourly Water Consumption Records")
plt.xlabel("Hour of Day (UTC)")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("data/processed/hourly_records.png")
plt.show()

# 2. Daily record distribution
daily = df.groupby("day_name").size()

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

daily = daily.reindex(day_order)

plt.figure(figsize=(10, 5))
daily.plot(kind="bar")
plt.title("Water Records by Day of Week")
plt.xlabel("Day")
plt.ylabel("Number of Records")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("data/processed/weekday_records.png")
plt.show()

# Print results
print("\n===== HOURLY RECORDS =====")
print(hourly)

print("\n===== DAY-WISE RECORDS =====")
print(daily)

print("\n===== EDA STEP 2 COMPLETED =====")
