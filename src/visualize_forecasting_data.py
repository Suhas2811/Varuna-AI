
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "forecasting_daily_dataset.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

df = pd.read_csv(DATA_FILE, parse_dates=["date"])

for sensor, group in df.groupby("sensor_id"):

    group = group.sort_values("date").copy()

    # Create a complete daily calendar
    full_dates = pd.date_range(
        start=group["date"].min(),
        end=group["date"].max(),
        freq="D"
    )

    # Missing dates remain NaN, not zero
    daily_series = (
        group.set_index("date")["daily_consumption"]
        .reindex(full_dates)
    )

    plt.figure(figsize=(12, 4))

    plt.plot(
        daily_series.index,
        daily_series.values,
        linewidth=0.8
    )

    plt.title(f"Daily Water Consumption - {sensor}")
    plt.xlabel("Date")
    plt.ylabel("Consumption (Litres)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file = (
        OUTPUT_DIR / f"{sensor}_daily_consumption_corrected.png"
    )

    plt.savefig(output_file, dpi=150)
    plt.close()

    print("Saved:", output_file)

print("\nCorrected plots generated successfully.")
