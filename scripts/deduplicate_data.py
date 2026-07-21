import os
import json
from datetime import datetime

import numpy as np
import pandas as pd


def detect_exact_duplicates(df):
    """
    Find rows where all values are identical.

    Returns:
        Tuple of (count, duplicate_rows_dataframe)
    """
    exact_dups = df.duplicated().sum()

    dup_rows = df[df.duplicated(keep=False)].sort_values(
        by=df.columns.tolist()
    )

    print("\nEXACT DUPLICATE DETECTION")
    print("=" * 60)
    print(f"Exact duplicates found: {exact_dups}")
    print(f"Total duplicate rows (including originals): {len(dup_rows)}")

    if len(dup_rows) > 0:
        print("\nSample duplicate rows:")
        print(dup_rows.head(10).to_string())

    return exact_dups, dup_rows


def detect_near_duplicates(df, key_columns):
    """
    Find rows with duplicate key values.
    """
    duplicate_keys = df[df.duplicated(subset=key_columns, keep=False)]

    print("\nNEAR DUPLICATE DETECTION")
    print("=" * 60)
    print(f"Records with duplicate keys: {len(duplicate_keys)}")
    print(
        f"Unique duplicate key groups: {len(duplicate_keys.groupby(key_columns))}"
    )

    if len(duplicate_keys) > 0:
        print("\nSample duplicate groups:")
        for keys, group in list(duplicate_keys.groupby(key_columns))[:3]:
            print(f"\nKey: {keys}")
            print(group.to_string())

    return duplicate_keys


def remove_exact_duplicates(df, keep="first"):
    """
    Remove exact duplicate rows.
    """
    rows_before = len(df)

    df_dedup = df.drop_duplicates(keep=keep)

    rows_after = len(df_dedup)
    rows_removed = rows_before - rows_after
    removal_pct = (rows_removed / rows_before) * 100

    print("\nEXACT DUPLICATE REMOVAL")
    print("=" * 60)
    print(f"Keep Strategy : {keep}")
    print(f"Rows Before   : {rows_before}")
    print(f"Rows After    : {rows_after}")
    print(f"Rows Removed  : {rows_removed} ({removal_pct:.2f}%)")

    return df_dedup


def remove_near_duplicates(
    df,
    key_columns,
    keep_strategy="most_complete",
):
    """
    Remove near duplicates.
    """

    rows_before = len(df)

    if keep_strategy == "most_complete":

        def keep_most_complete(group):
            null_counts = group.isnull().sum(axis=1)
            best_idx = null_counts.idxmin()
            return group.loc[[best_idx]]

        df_dedup = (
            df.groupby(key_columns, group_keys=False)
            .apply(keep_most_complete)
            .reset_index(drop=True)
        )

    elif keep_strategy == "last":
        df_dedup = df.drop_duplicates(
            subset=key_columns,
            keep="last",
        )

    else:
        df_dedup = df.drop_duplicates(
            subset=key_columns,
            keep="first",
        )

    rows_after = len(df_dedup)
    rows_removed = rows_before - rows_after
    removal_pct = (rows_removed / rows_before) * 100

    print("\nNEAR DUPLICATE REMOVAL")
    print("=" * 60)
    print(f"Strategy      : {keep_strategy}")
    print(f"Rows Before   : {rows_before}")
    print(f"Rows After    : {rows_after}")
    print(f"Rows Removed  : {rows_removed} ({removal_pct:.2f}%)")

    return df_dedup


def log_removed_duplicates(df_original, df_dedup):
    """
    Save removed records.
    """
    removed_mask = ~df_original.index.isin(df_dedup.index)
    removed_records = df_original[removed_mask]

    os.makedirs("output", exist_ok=True)

    removed_records.to_csv(
        "output/removed_duplicates_audit.csv",
        index=False,
    )

    audit_summary = {
        "timestamp": datetime.now().isoformat(),
        "removed_records": int(len(removed_records)),
        "reason": "Duplicate removal",
        "audit_file": "output/removed_duplicates_audit.csv",
    }

    with open(
        "output/dedup_audit_summary.json",
        "w",
    ) as f:
        json.dump(audit_summary, f, indent=4)

    print("\nAUDIT LOG CREATED")

    return removed_records, audit_summary


def compare_before_after(df_original, df_dedup):
    comparison = {
        "rows_before": len(df_original),
        "rows_after": len(df_dedup),
        "rows_removed": len(df_original) - len(df_dedup),
        "removal_percentage": round(
            (
                (len(df_original) - len(df_dedup))
                / len(df_original)
            )
            * 100,
            2,
        ),
        "columns": len(df_original.columns),
        "nulls_before": int(df_original.isnull().sum().sum()),
        "nulls_after": int(df_dedup.isnull().sum().sum()),
        "timestamp": datetime.now().isoformat(),
    }

    print("\nFINAL SUMMARY")
    print("=" * 60)

    for key, value in comparison.items():
        print(f"{key} : {value}")

    with open(
        "output/dedup_summary.json",
        "w",
    ) as f:
        json.dump(comparison, f, indent=4)

    return comparison


def main():
    os.makedirs("output", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    df_original = pd.read_csv(
        "data/raw/data_with_dupes.csv"
    )

    print("=" * 70)
    print("STARTING DEDUPLICATION")
    print("=" * 70)

    detect_exact_duplicates(df_original)

    detect_near_duplicates(
        df_original,
        ["customer_id", "transaction_date"],
    )

    df_exact = remove_exact_duplicates(
        df_original,
        keep="first",
    )

    df_final = remove_near_duplicates(
        df_exact,
        ["customer_id", "transaction_date"],
        keep_strategy="most_complete",
    )

    log_removed_duplicates(
        df_original,
        df_final,
    )

    compare_before_after(
        df_original,
        df_final,
    )

    df_final.to_csv(
        "data/processed/deduplicated_data.csv",
        index=False,
    )

    print("\nDeduplicated data saved successfully.")


if __name__ == "__main__":
    main()