
import pandas as pd
from pathlib import Path

# Load data
data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Select toilet sensors
toilets = df[df["attached_to"] == "Toilet"].copy()

# Create monthly grouping
toilets["month"] = toilets["timestamp"].dt.strftime("%Y-%m")

# Separate S0212 and other toilet sensors
s0212 = toilets[toilets["sensor_id"] == "S0212"]

other = toilets[toilets["sensor_id"] != "S0212"]

# Monthly comparison
s0212_monthly = s0212.groupby("month").agg(
    records=("value", "count"),
    mean_value=("value", "mean"),
    high_values=("value", lambda x: (x > 0.10).sum())
)

other_monthly = other.groupby("month").agg(
    records=("value", "count"),
    mean_value=("value", "mean"),
    high_values=("value", lambda x: (x > 0.10).sum())
)

comparison = s0212_monthly.join(
    other_monthly,
    how="outer",
    lsuffix="_S0212",
    rsuffix="_Other"
)

print("\n===== MONTHLY TOILET SENSOR COMPARISON =====")
print(comparison.loc[
    ["2021-09", "2021-10", "2021-11",
     "2022-03", "2022-04", "2022-05",
     "2022-06", "2022-07", "2022-08"]
].round(4).to_string())

print("\n===== INVESTIGATION COMPLETED =====")
