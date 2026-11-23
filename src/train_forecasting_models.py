
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "forecasting_features.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
RESULT_FILE = OUTPUT_DIR / "model_evaluation_results.csv"


# Load dataset
df = pd.read_csv(INPUT_FILE)
df["date"] = pd.to_datetime(df["date"], utc=True)


# Features and target
FEATURE_COLUMNS = [
    "day_of_week",
    "day_of_month",
    "month",
    "lag_1",
    "lag_7",
    "rolling_mean_7",
    "rolling_mean_14"
]

TARGET_COLUMN = "daily_consumption"

# Remove rows with incomplete features
df = df.dropna(
    subset=FEATURE_COLUMNS + [TARGET_COLUMN]
).copy()


# Define models
models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


results = []

print("========== MODEL TRAINING ==========")

# Train and evaluate separately for each sensor
for sensor_id, sensor_df in df.groupby("sensor_id"):

    sensor_df = sensor_df.sort_values("date").copy()

    # Chronological 80:20 split
    split_index = int(len(sensor_df) * 0.8)

    train_df = sensor_df.iloc[:split_index]
    test_df = sensor_df.iloc[split_index:]

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[TARGET_COLUMN]

    print(f"\nSensor: {sensor_id}")
    print("Training records:", len(train_df))
    print("Testing records:", len(test_df))

    for model_name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test, predictions
        )

        rmse = np.sqrt(
            mean_squared_error(y_test, predictions)
        )

        r2 = r2_score(
            y_test, predictions
        )

        results.append({
            "sensor_id": sensor_id,
            "model": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "training_records": len(train_df),
            "testing_records": len(test_df)
        })

        print(f"\n{model_name}")
        print(f"MAE:  {mae:.6f}")
        print(f"RMSE: {rmse:.6f}")
        print(f"R2:   {r2:.4f}")


# Save results
results_df = pd.DataFrame(results)

results_df.to_csv(
    RESULT_FILE,
    index=False
)

print("\n========== TRAINING COMPLETED ==========")
print("Total model evaluations:", len(results_df))
print("Results saved to:")
print(RESULT_FILE)
