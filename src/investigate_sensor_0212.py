
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Select S0212 and other toilet sensors
sensor_0212 = df[df["sensor_id"] == "S0212"].copy()

other_toilets = df[
    (df["attached_to"] == "Toilet") &
    (df["sensor_id"] != "S0212")
].copy()

print("\n===== SENSOR S0212 PROFILE =====")

print("Total records:", len(sensor_0212))
print("Fixture:", sensor_0212["attached_to"].iloc[0])
print("Water types:")
print(sensor_0212["type"].value_counts())

print("\nValue statistics:")
print(sensor_0212["value"].describe())

print("\nHigh-value records:")
print((sensor_0212["value"] > 0.10).sum())

print("\n===== OTHER TOILET SENSORS =====")

print("Number of sensors:", other_toilets["sensor_id"].nunique())

print("\nValue statistics:")
print(other_toilets["value"].describe())

print("\nHigh-value records:")
print((other_toilets["value"] > 0.10).sum())

print("\n===== SENSOR S0212 MONTHLY ACTIVITY =====")

print(
    sensor_0212.groupby(
        sensor_0212["timestamp"].dt.to_period("M")
    ).agg(
        records=("value", "count"),
        mean_value=("value", "mean"),
        high_values=("value", lambda x: (x > 0.10).sum())
    ).tail(20)
)

print("\n===== INVESTIGATION COMPLETED =====")
