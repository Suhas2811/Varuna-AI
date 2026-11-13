
from pathlib import Path
import pandas as pd

# Locate project directory
project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data" / "raw"

# Find CSV file
csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found in data/raw.")

file_path = csv_files[0]

print("Loading:", file_path.name)

# Load semicolon-separated CSV
df = pd.read_csv(file_path, sep=";", encoding="utf-8-sig")

# 1. Measurement statistics
print("\n===== VALUE STATISTICS =====")
print(df[["value", "aggregated_value"]].describe())

# 2. Water types
print("\n===== WATER TYPES =====")
print(df["type"].value_counts(dropna=False))

# 3. Fixture types
print("\n===== FIXTURE TYPES =====")
print(df["attached_to"].value_counts(dropna=False))

# 4. Room types
print("\n===== ROOM TYPES =====")
print(df["room_type"].value_counts(dropna=False))

# 5. Sensor information
print("\n===== SENSOR COUNT =====")
print("Unique sensors:", df["sensor_id"].nunique())
print(df["sensor_id"].value_counts().head(10))

# 6. Apartments
print("\n===== APARTMENTS =====")
print(df["apartment"].value_counts(dropna=False))

# 7. Clusters
print("\n===== CLUSTERS =====")
print(df["cluster_name"].value_counts(dropna=False))

# 8. Timestamp range
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

print("\n===== TIME RANGE =====")
print("Start:", df["timestamp"].min())
print("End:", df["timestamp"].max())

# 9. Measurement relationship
print("\n===== VALUE CORRELATION =====")
print(df[["value", "aggregated_value"]].corr())

print("\n===== ANALYSIS COMPLETED =====")
