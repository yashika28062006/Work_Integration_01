import pandas as pd
import numpy as np
import json
import os


def analyze_missing_values(df):
    """
    Compute null counts and percentages before treatment.
    """

    missing_analysis = pd.DataFrame({
        "column": df.columns,
        "null_count": df.isnull().sum().values,
        "null_percentage": (df.isnull().sum() / len(df) * 100).round(2).values,
        "data_type": df.dtypes.values,
        "null_meaning": [
            "Unique customer identifier",
            "Customer name",
            "Customer email",
            "Purchase amount",
            "Product category",
            "Quantity purchased",
            "Customer region",
            "Last update date"
        ]
    })

    print("=" * 70)
    print("BEFORE IMPUTATION - Missing Value Analysis")
    print("=" * 70)
    print(missing_analysis.to_string(index=False))

    print(f"\nTotal rows       : {len(df)}")
    print(f"Total columns    : {len(df.columns)}")
    print(f"Total cells      : {len(df) * len(df.columns)}")
    print(f"Missing cells    : {df.isnull().sum().sum()}")
    print("=" * 70)

    return missing_analysis


def drop_rows_with_nulls(df, critical_cols):
    """Drop rows with nulls in critical columns."""

    rows_before = len(df)

    df_imputed = df.dropna(subset=critical_cols)

    rows_dropped = rows_before - len(df_imputed)

    print(f"✓ Dropped {rows_dropped} row(s) with nulls in {critical_cols}")

    return df_imputed


def impute_mean_median(df, numerical_cols, strategy="median"):
    """Fill numerical nulls with mean or median."""

    df_imputed = df.copy()

    for col in numerical_cols:

        if df_imputed[col].isnull().sum() > 0:

            if strategy == "median":
                fill_value = df_imputed[col].median()
            else:
                fill_value = df_imputed[col].mean()

            count = df_imputed[col].isnull().sum()

            df_imputed[col] = df_imputed[col].fillna(fill_value)

            print(f"✓ {col}: filled {count} null(s) with {strategy} ({fill_value:.2f})")

    return df_imputed


def impute_mode(df, categorical_cols):
    """Fill categorical nulls with mode."""

    df_imputed = df.copy()

    for col in categorical_cols:

        if df_imputed[col].isnull().sum() > 0:

            mode_value = df_imputed[col].mode()[0]

            count = df_imputed[col].isnull().sum()

            df_imputed[col] = df_imputed[col].fillna(mode_value)

            print(f"✓ {col}: filled {count} null(s) with mode ({mode_value})")

    return df_imputed


def impute_forward_fill(df, time_series_cols):
    """Forward fill time-series columns."""

    df_imputed = df.copy()

    for col in time_series_cols:

        if df_imputed[col].isnull().sum() > 0:

            count = df_imputed[col].isnull().sum()

            df_imputed[col] = df_imputed[col].ffill()

            print(f"✓ {col}: forward-filled {count} null(s)")

    return df_imputed


def document_imputation_decisions(df_original):
    """Save business reasoning for imputation."""

    decisions = {
        "amount": {
            "column_type": "Numerical",
            "strategy": "Median",
            "value_used": float(df_original["amount"].median()),
            "business_reasoning": "Median avoids influence from outliers.",
            "risk_assessment": "Low"
        },
        "quantity": {
            "column_type": "Numerical",
            "strategy": "Median",
            "value_used": float(df_original["quantity"].median()),
            "business_reasoning": "Median preserves the typical quantity.",
            "risk_assessment": "Low"
        },
        "name": {
            "column_type": "Categorical",
            "strategy": "Mode",
            "business_reasoning": "Most frequent value preserves distribution.",
            "risk_assessment": "Low"
        },
        "region": {
            "column_type": "Categorical",
            "strategy": "Mode",
            "business_reasoning": "Most common region maintains consistency.",
            "risk_assessment": "Low"
        },
        "email": {
            "column_type": "Critical Identifier",
            "strategy": "Drop Rows",
            "business_reasoning": "Records without email are incomplete.",
            "risk_assessment": "Low"
        },
        "last_updated": {
            "column_type": "Time Series",
            "strategy": "Forward Fill",
            "business_reasoning": "Previous timestamp assumed valid.",
            "risk_assessment": "Medium"
        }
    }

    os.makedirs("output", exist_ok=True)

    with open("output/imputation_decisions.json", "w") as f:
        json.dump(decisions, f, indent=4)

    print("\n✓ Imputation decisions saved to output/imputation_decisions.json")


def validate_imputation(df_before, df_after):
    """Compare before and after metrics."""

    print("\n" + "=" * 70)
    print("AFTER IMPUTATION - Validation Report")
    print("=" * 70)

    print(f"Rows before : {len(df_before)}")
    print(f"Rows after  : {len(df_after)}")
    print(f"Rows removed: {len(df_before)-len(df_after)}")

    print(f"\nNulls before : {df_before.isnull().sum().sum()}")
    print(f"Nulls after  : {df_after.isnull().sum().sum()}")

    print("\nRemaining Missing Values")

    print(pd.DataFrame({
        "column": df_after.columns,
        "null_count": df_after.isnull().sum().values,
        "null_percentage": (
            df_after.isnull().sum() / len(df_after) * 100
        ).round(2).values
    }).to_string(index=False))

    print("=" * 70)


def main():

    df = pd.read_csv("data/raw/missing_data.csv")

    analyze_missing_values(df)

    print("\nApplying Missing Value Handling...\n")

    df_before = df.copy()

    df = drop_rows_with_nulls(df, ["customer_id", "email"])

    df = impute_mean_median(
        df,
        ["amount", "quantity"],
        strategy="median"
    )

    df = impute_mode(
        df,
        ["name", "category", "region"]
    )

    df = impute_forward_fill(
        df,
        ["last_updated"]
    )

    document_imputation_decisions(df_before)

    validate_imputation(df_before, df)

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(
        "data/processed/cleaned_data.csv",
        index=False
    )

    print("\n✓ Cleaned data saved to data/processed/cleaned_data.csv")


if __name__ == "__main__":
    main()