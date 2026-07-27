import pandas as pd
import os
from datetime import datetime

# ==========================================================
# Create folders if they don't exist
# ==========================================================
os.makedirs("data/processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================
df = pd.read_csv("data/raw/transaction_data.csv")

print("=" * 70)
print("ORIGINAL DATASET")
print("=" * 70)
print(df)

# ==========================================================
# TASK 1 - Parse Datetime
# ==========================================================
print("\n" + "=" * 70)
print("TASK 1 - DATETIME PARSING")
print("=" * 70)

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    format="%Y-%m-%d %H:%M:%S"
)

print(df.dtypes)

# ==========================================================
# TASK 2 - Extract Date Features
# ==========================================================
print("\n" + "=" * 70)
print("TASK 2 - DATE FEATURE EXTRACTION")
print("=" * 70)

df["day_of_week"] = df["transaction_date"].dt.day_name()
df["day_number"] = df["transaction_date"].dt.dayofweek
df["hour"] = df["transaction_date"].dt.hour
df["week_number"] = df["transaction_date"].dt.isocalendar().week
df["month"] = df["transaction_date"].dt.month
df["quarter"] = df["transaction_date"].dt.quarter

print(df[
    [
        "transaction_date",
        "day_of_week",
        "hour",
        "week_number",
        "month",
        "quarter",
    ]
])

# ==========================================================
# TASK 3 - Days Since Purchase
# ==========================================================
print("\n" + "=" * 70)
print("TASK 3 - ELAPSED TIME")
print("=" * 70)

today = pd.Timestamp.now()

df["days_since_purchase"] = (
    today - df["transaction_date"]
).dt.days

print(df[
    [
        "customer_id",
        "transaction_date",
        "days_since_purchase",
    ]
])

# ==========================================================
# TASK 4 - Weekly Revenue using Resample
# ==========================================================
print("\n" + "=" * 70)
print("TASK 4 - WEEKLY RESAMPLING")
print("=" * 70)

weekly = (
    df.set_index("transaction_date")["amount"]
    .resample("W")
    .sum()
)

print(weekly)

# ==========================================================
# TASK 5 - Monthly Revenue
# ==========================================================
print("\n" + "=" * 70)
print("TASK 5 - MONTHLY RESAMPLING")
print("=" * 70)

monthly = (
    df.set_index("transaction_date")["amount"]
    .resample("ME")
    .sum()
)

print(monthly)

# ==========================================================
# Save Outputs
# ==========================================================
df.to_csv(
    "data/processed/datetime_features.csv",
    index=False,
)

weekly.to_csv(
    "output/weekly_revenue.csv",
    header=["weekly_revenue"],
)

monthly.to_csv(
    "output/monthly_revenue.csv",
    header=["monthly_revenue"],
)

summary = {
    "rows": len(df),
    "columns": len(df.columns),
    "date_range_start": str(df["transaction_date"].min()),
    "date_range_end": str(df["transaction_date"].max()),
    "generated_at": str(datetime.now()),
}

pd.Series(summary).to_json(
    "output/datetime_summary.json",
    indent=4,
)

print("\n" + "=" * 70)
print("DATETIME TRANSFORMATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated Files:")
print("data/processed/datetime_features.csv")
print("output/weekly_revenue.csv")
print("output/monthly_revenue.csv")
print("output/datetime_summary.json")