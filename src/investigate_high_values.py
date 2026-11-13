
import pandas as pd
from pathlib import Path

# Load dataset
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df["date"] = df["timestamp"].dt.date

# Select high values
high = df[df["value"] > 0.10].copy()

print("\n===== HIGH VALUE RECORDS =====")
print("Total records above 0.10 L:", len(high))

print("\n===== HIGH VALUES BY DATE =====")
print(
    high.groupby("date")
    .size()
    .sort_values(ascending=False)
    .head(20)
)

print("\n===== HIGH VALUES BY FIXTURE =====")
print(high["attached_to"].value_counts())

print("\n===== HIGH VALUES BY WATER TYPE =====")
print(high["type"].value_counts())

print("\n===== HIGH VALUES BY YEAR =====")
print(high["timestamp"].dt.year.value_counts().sort_index())

print("\n===== HIGHEST 20 RECORDS =====")
columns = [
    "timestamp",
    "sensor_id",
    "attached_to",
    "type",
    "value",
    "aggregated_value"
]

print(
    df.nlargest(20, "value")[columns].to_string(index=False)
)

print("\n===== INVESTIGATION COMPLETED =====")
