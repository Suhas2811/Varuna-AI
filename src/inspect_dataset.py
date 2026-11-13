import pandas as pd
from pathlib import Path

# Dataset location
data_path = Path("data/raw/HSB_Living_Lab_Water_Consumption_Anonymized.csv")

print("Loading water consumption dataset...")

# Read semicolon-separated CSV
df = pd.read_csv(data_path, sep=";")

print("\n========== DATASET OVERVIEW ==========")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())

print("\n========== DATASET INFORMATION ==========")
df.info()
