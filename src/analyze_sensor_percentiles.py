
import pandas as pd
from pathlib import Path

data_folder = Path("data/raw")
csv_file = next(data_folder.glob("*.csv"))

df = pd.read_csv(csv_file, sep=";", encoding="utf-8-sig")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

toilets = df[df["attached_to"] == "Toilet"].copy()
toilets["month"] = toilets["timestamp"].dt.strftime("%Y-%m")

for sensor_name, data in [
    ("S0212", toilets[toilets["sensor_id"] == "S0212"]),
    ("Other toilet sensors", toilets[toilets["sensor_id"] != "S0212"])
]:
    print(f"\n===== {sensor_name} =====")

    print(
        data.groupby("month")["value"]
        .agg(
            count="count",
            median="median",
            percentile_75=lambda x: x.quantile(0.75),
            percentile_95=lambda x: x.quantile(0.95),
            maximum="max"
        )
        .loc[lambda x: x.index.isin([
            "2021-09", "2021-10", "2021-11",
            "2022-03", "2022-04", "2022-05",
            "2022-06", "2022-07", "2022-08"
        ])]
        .round(4)
    )

print("\n===== INVESTIGATION COMPLETED =====")
